import os
import requests
from flask import Flask, render_template, request, Response
import io
import sys
import contextlib
import builtins

# Some Python environments (or older stdlib snapshots) may not provide
# contextlib.redirect_stdin. Provide a small compatibility shim so the
# rest of the code can always use contextlib.redirect_stdin.
if not hasattr(contextlib, "redirect_stdin"):
    class _RedirectStdin:
        def __init__(self, new_stdin):
            self._new_stdin = new_stdin
            self._old_stdin = None

        def __enter__(self):
            self._old_stdin = sys.stdin
            sys.stdin = self._new_stdin
            return self._new_stdin

        def __exit__(self, exc_type, exc, tb):
            sys.stdin = self._old_stdin

    contextlib.redirect_stdin = _RedirectStdin

# 대신하는 입력 교체용 컨텍스트매니저: 제출 폼의 stdin 텍스트를
# 줄 단위로 소비하는 임시 input() 구현으로 교체합니다.
class RedirectInput:
    def __init__(self, text):
        # splitlines()는 빈 문자열에 대해 빈 리스트를 반환합니다.
        self._lines = text.splitlines()
        self._iter = iter(self._lines)
        self._old_input = None

    def __enter__(self):
        self._old_input = builtins.input

        def _inp(prompt=None):
            try:
                return next(self._iter)
            except StopIteration:
                # 원래 input()이 더 이상 읽을 게 없으면 EOFError를 발생시킵니다.
                raise EOFError("No more input")

        builtins.input = _inp
        return builtins.input

    def __exit__(self, exc_type, exc, tb):
        builtins.input = self._old_input


# 간단한 설명:
# - 이 앱은 웹에서 파이썬 답안을 받아서 내부에서 실행(메모리 모듈) 후
#   로컬 채점기(test_checker.run_week)를 호출해 채점 결과를 보여주고
#   (옵션) GitHub 이슈를 생성합니다.

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # GitHub API 호출에 사용할 토큰 (환경변수 권장)
GITHUB_REPO = "reomoon/study_python"  # 이 리포지토리에 이슈를 생성합니다.

app = Flask(__name__)

# 기본 문제 로드는 요청 시 처리합니다. (동적 주차 선택 지원)
PROBLEM = "문제 파일을 불러올 수 없습니다."  # 템플릿 렌더링용 기본값

# 각 주차별 수업(클래스) 이름: 선택창 옆에 표시됩니다.
# 필요하면 여기 문구를 수정하세요.
WEEK_OPTIONS = [
    ('1', '변수'),
    ('2', '자료형'),
    ('3', '출력/입력'),
    ('4', '조건문/예외처리'),
    ('5', '반복문'),
    ('6', '함수/모듈'),
    ('9', '파일 입출력'),
    ('10', '클래스'),
]

# 채점 스크립트
HTML = '''
<h2>Python 기초 스터디 자동 채점기</h2>
'''
# 템플릿 파일명 사용
TEMPLATE_NAME = 'index.html'

@app.route("/", methods=["GET", "POST"])
def index():
    # result: 템플릿에 표시할 채점/오류 메시지
    result = ""
    # selected_week: GET 쿼리 또는 POST 폼에서 선택된 주차 (기본 1)
    selected_week = request.args.get('week', '1')
    student_output = ''
    checker_output = ''
    submitted_code = ''
    if request.method == "POST":
        # Use .get to avoid BadRequestKeyError which results in HTTP 400 when a field is missing.
        username = request.form.get("username", "").strip()
        code = request.form.get("code", "")
        week = request.form.get("week", "1")
        # Basic validation: if required fields are missing, show a friendly message instead of HTTP 400.
        if not username or not code:
            result = "❌ 제출 요청에 필수 항목이 없습니다. 브라우저에서 '이름'과 '답안 코드'가 전송되는지 확인하세요. 네트워크 탭의 Form Data를 확인하면 문제 원인을 알 수 있습니다."
            try:
                with open(f"problem/problem_week{selected_week}.html", 'r', encoding='utf-8') as pf:
                    PROBLEM_TXT = pf.read()
            except Exception as e:
                PROBLEM_TXT = f"문제 파일을 불러올 수 없습니다: {e}"
            return render_template(TEMPLATE_NAME, problem=PROBLEM_TXT, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS, student_output=student_output, checker_output=checker_output, submitted_code=submitted_code)
        selected_week = str(week)
        submitted_code = code
        # 동적 문제 로드
        problem_path = f"problem/problem_week{week}.html"
        try:
            with open(problem_path, 'r', encoding='utf-8') as pf:
                PROBLEM_TXT = pf.read()
        except Exception as e:
            PROBLEM_TXT = f"문제 파일을 불러올 수 없습니다: {e}"
        # 제출 코드를 파일로 저장 (Vercel은 읽기 전용 파일 시스템이므로 파일 쓰기 금지)
        # 대신 메모리 모듈을 생성해 `week{N}_variable` 이름으로 sys.modules에 주입합니다.
        import types
        module_name = f'week{week}_variable'
        module = types.ModuleType(module_name)
        # 학생 코드의 실행 출력을 캡처해서 결과에 보여주기 위해 stdout을 리디렉트합니다.
        student_output = ''
        try:
            import contextlib
            buf_exec = io.StringIO()
            stdin_text = request.form.get('stdin', '')
            # Provide the supplied stdin to input() calls using RedirectInput
            try:
                with contextlib.redirect_stdout(buf_exec), RedirectInput(stdin_text):
                    exec(code, module.__dict__)
            except EOFError as ee:
                # Provide a clearer message for missing input
                student_output = buf_exec.getvalue()
                result = f"❌ 제출 코드 실행 중 에러: 입력이 필요합니다 (EOF).\n입력값이 필요한 경우 제출 폼의 '표준 입력' 칸에 값을 넣어주세요.\n\n에러: {ee}"
                return render_template(TEMPLATE_NAME, problem=PROBLEM_TXT, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS, student_output=student_output, checker_output=checker_output, submitted_code=submitted_code)
            student_output = buf_exec.getvalue()
            # 제출 원본을 모듈에 보관하면 채점기가 메모리 모듈의 출력/주석을 검사할 수 있습니다.
            module.__source__ = code
            sys.modules[module_name] = module
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            if isinstance(e, IndentationError):
                result = f"❌ 제출 코드 실행 중 <b>들여쓰기 오류(IndentationError)</b>가 발생했습니다.<br>코드의 각 줄 앞에 불필요한 공백이나 탭이 있는지 확인하세요.<br><pre>{e}\n\n{tb}</pre>"
            else:
                result = f"❌ 제출 코드 실행 중 에러 발생:<br><pre>{e}\n\n{tb}</pre>"
            return render_template(TEMPLATE_NAME, problem=PROBLEM_TXT, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS, student_output=student_output, checker_output=checker_output, submitted_code=submitted_code)

        # test_checker.py 실행 (서버리스 환경 친화적 방식으로 변경)
        # 이전에는 subprocess로 외부 프로세스를 실행했음.
        # Vercel 같은 서버리스 환경에서는 subprocess 사용이 제한되거나 실패할 수 있으므로,
        # test_checker 모듈을 직접 import하고 stdout을 캡처하여 실행하도록 변경합니다.
        try:
            import importlib
            import importlib.util
            import contextlib
            from io import StringIO

            buf = StringIO()
            # test_checker를 임포트(또는 reload)하고 run_week(week)을 호출하여
            # stdout으로 출력되는 채점 메시지를 캡처합니다.
            with contextlib.redirect_stdout(buf):
                # 이미 임포트되어 있을 수 있으므로 reload로 최신 상태 반영
                if 'test_checker' in sys.modules:
                    importlib.reload(sys.modules['test_checker']).run_week(week)
                else:
                    import test_checker
                    importlib.reload(test_checker)
                    test_checker.run_week(week)
            checker_output = buf.getvalue()
            result = f"<b>자동 채점 결과:</b><br>✅ 정상 실행!"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            output = f"{e}\n\n{tb}"
            result = f"❌ 자동 채점 중 에러 발생:<br><pre>{output}</pre>"

        # GitHub 이슈 생성
        # GitHub 이슈 생성: 토큰이 있으면 채점 결과와 원본 코드를 리포에 등록
        if GITHUB_TOKEN:
            issue_title = f"[{week}주차] {username} 답안 제출"
            issue_body = f"""**이름:** {username}\n\n**주차:** {week}주차\n\n**답안 코드:**\n```python\n{code}\n```\n\n**학생 코드 출력:**\n```
{student_output}
```\n\n**자동 채점 결과:**\n```
{checker_output}
```"""
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {"title": issue_title, "body": issue_body}
            r = requests.post(f"https://api.github.com/repos/reomoon/study_python/issues", json=data, headers=headers)
            if r.status_code == 201:
                # API가 반환한 생성된 이슈의 HTML URL을 가져와서 사용자에게 링크로 제공
                try:
                    issue_url = r.json().get('html_url')
                except Exception:
                    issue_url = None
                    if issue_url:
                    # Make the issue link text smaller so it doesn't dominate the result area
                        result += f"<br>✅ GitHub 이슈가 성공적으로 생성되었습니다!<br>🔗 이슈 확인: <span style=\"font-size:0.9em;\"><a href=\"{issue_url}\" target=\"_blank\">{issue_url}</a></span>"
                else:
                    result += f"<br>✅ GitHub 이슈가 성공적으로 생성되었습니다!<br>🔗 이슈 목록: <span style=\"font-size:0.9em;\">https://github.com/{GITHUB_REPO}/issues</span>"
            else:
                result += f"<br>❌ GitHub 이슈 생성 실패: {r.text}"
        else:
            result += "<br>⚠️ GitHub 토큰이 설정되어 있지 않습니다."

    # 렌더링 결과 반환
    # GET이든 POST이든 selected_week에 따라 문제 로드
    # 요청된 주차의 문제 파일을 로드해서 템플릿에 전달
    try:
        with open(f"problem/problem_week{selected_week}.html", 'r', encoding='utf-8') as pf:
            PROBLEM_TXT = pf.read()
    except Exception as e:
        PROBLEM_TXT = f"문제 파일을 불러올 수 없습니다: {e}"

    return render_template(TEMPLATE_NAME, problem=PROBLEM_TXT, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS, student_output=student_output, checker_output=checker_output, submitted_code=submitted_code)
# 로컬에서는 5555, Vercel에서는 자동 포트로 동작
# 로컬 푸시할때는 vercel 환경에서 실행 안되니 주석처리
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5555))
#     app.run(port=port)


@app.route('/example')
def example():
    week = request.args.get('week', '1')
    path = f"examples/week{week}_example.py"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/plain; charset=utf-8')
    except Exception as e:
        return Response(f"# 예제 파일을 찾을 수 없습니다: {e}", mimetype='text/plain; charset=utf-8')
    
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))
    app.run(port=port)

