import os
import requests
from flask import Flask, render_template_string, request
import io
import sys

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
    ('1', '변수와 출력'),
    ('2', '데이터 타입과 연산'),
    ('3', '조건문과 반복문'),
    ('4', '함수 기초'),
    ('5', '자료구조 기초'),
    ('6', '파일 입출력'),
    ('7', '모듈과 패키지'),
    ('8', '예외 처리와 테스트'),
    ('9', '객체지향 기초'),
    ('10','간단한 프로젝트')
]

# 채점 스크립트
HTML = '''
<h2>Python 기초 스터디 자동 채점기</h2>
<div style="background:#f8f9fa;padding:15px;border-radius:10px;margin-bottom:20px;">{{ problem|safe }}</div>
<form method="post" onsubmit="document.getElementById('code').value = editor.getValue();">
    이름: <input name="username" required><br><br>
    주차: <select name="week" onchange="onWeekChange(this.value)"> <!-- 선택 시 GET으로 재요청해 문제를 변경 -->
        {% for k, label in week_options %}
            <option value="{{ k }}" {% if selected_week == k %}selected{% endif %}>{{ k }}주차 - {{ label }}</option>
        {% endfor %}
    </select><br><br>
    답안 코드:<br>
    <textarea id="code" name="code" style="display:none"></textarea>
            <div id="editor" style="border:1px solid #ccc; border-radius:5px; height:350px; width:800px; margin-bottom:10px; overflow-y:auto;"></div><br>
    <button type="submit">제출</button>
</form>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/addon/edit/closebrackets.min.js"></script>
<script>
var editor = CodeMirror(document.getElementById('editor'), {
        value: '',
        mode: 'python',
        theme: 'default',
        lineNumbers: true,
        indentUnit: 4,
        indentWithTabs: true,
        autoCloseBrackets: true,
        tabSize: 4,
        extraKeys: {
                Tab: function(cm) { cm.replaceSelection('    ', 'end'); }
        }
});
</script>
<script>
function onWeekChange(v) {
    // reload the page with selected week as query param (GET)
    const params = new URLSearchParams(window.location.search);
    params.set('week', v);
    window.location.search = params.toString();
}
</script>
{% if result %}
<hr>
<b>결과:</b><br>
{{ result|safe }}
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    # result: 템플릿에 표시할 채점/오류 메시지
    result = ""
    # selected_week: GET 쿼리 또는 POST 폼에서 선택된 주차 (기본 1)
    selected_week = request.args.get('week', '1')
    if request.method == "POST":
        username = request.form["username"]
        code = request.form["code"]
        week = request.form["week"]
        selected_week = str(week)
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
            with contextlib.redirect_stdout(buf_exec):
                exec(code, module.__dict__)
            student_output = buf_exec.getvalue()
            # 제출 원본을 모듈에 보관하면 채점기가 메모리 모듈의 출력/주석을 검사할 수 있습니다.
            module.__source__ = code
            sys.modules[module_name] = module
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            # 실행 중 예외가 발생하면 즉시 사용자에게 보여주고 중단
            result = f"❌ 제출 코드 실행 중 에러 발생:<br><pre>{e}\n\n{tb}</pre>"
            return render_template_string(HTML, problem=PROBLEM, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS)

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
            output = buf.getvalue()
            # 학생 코드 출력과 채점 출력을 함께 보여줍니다.
            combined = """
학생 코드 출력:
{student}

채점기 출력:
{checker}
""".format(student=student_output, checker=output)
            result = f"<b>자동 채점 결과:</b><br><pre>{combined}</pre><br>✅ 정상 실행!"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            output = f"{e}\n\n{tb}"
            result = f"❌ 자동 채점 중 에러 발생:<br><pre>{output}</pre>"

        # GitHub 이슈 생성
        # GitHub 이슈 생성: 토큰이 있으면 채점 결과와 원본 코드를 리포에 등록
        if GITHUB_TOKEN:
            issue_title = f"[{week}주차] {username} 답안 제출"
            issue_body = f"""**이름:** {username}\n\n**주차:** {week}주차\n\n**답안 코드:**\n```python\n{code}\n```\n\n**자동 채점 결과:**\n```
{output}
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
                    result += f"<br>✅ GitHub 이슈가 성공적으로 생성되었습니다!<br>🔗 이슈 확인: <a href=\"{issue_url}\" target=\"_blank\">{issue_url}</a>"
                else:
                    result += f"<br>✅ GitHub 이슈가 성공적으로 생성되었습니다!<br>🔗 이슈 목록: https://github.com/{GITHUB_REPO}/issues"
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

    return render_template_string(HTML, problem=PROBLEM_TXT, result=result, selected_week=selected_week, week_options=WEEK_OPTIONS)

# 로컬에서는 5555, Vercel에서는 자동 포트로 동작
# 로컬 푸시할때는 vercel 환경에서 실행 안되니 주석처리
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5555))
#     app.run(port=port)