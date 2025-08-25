import os
import requests
from flask import Flask, render_template_string, request
import io
import sys

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # 환경변수로 토큰 관리
GITHUB_REPO = "reomoon/study_python"

app = Flask(__name__)

# problem 폴더에서 불러와 문제를 출력
try:
    with open("problem/problem_week1.html", "r", encoding="utf-8") as f:
        PROBLEM = f.read()
except Exception as e:
    PROBLEM = f"문제 파일을 불러올 수 없습니다: {e}"

# 채점 스크립트
HTML = '''
<h2>Python 기초 스터디 자동 채점기</h2>
<div style="background:#f8f9fa;padding:15px;border-radius:10px;margin-bottom:20px;">{{ problem|safe }}</div>
<form method="post" onsubmit="document.getElementById('code').value = editor.getValue();">
    이름: <input name="username" required><br><br>
    주차: <select name="week">
        <option value="1">1주차</option>
        <option value="2">2주차</option>
        <option value="3">3주차</option>
        <option value="4">4주차</option>
        <option value="5">5주차</option>
        <option value="6">6주차</option>
        <option value="7">7주차</option>
        <option value="8">8주차</option>
        <option value="9">9주차</option>
        <option value="10">10주차</option>
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
{% if result %}
<hr>
<b>결과:</b><br>
{{ result|safe }}
{% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        username = request.form["username"]
        code = request.form["code"]
        week = request.form["week"]
        # 제출 코드를 파일로 저장 (Vercel은 읽기 전용 파일 시스템이므로 파일 쓰기 금지)
        # 대신 메모리 모듈을 생성해 `week1_variable` 이름으로 sys.modules에 주입합니다.
        import types
        module_name = 'week1_variable'
        module = types.ModuleType(module_name)
        try:
            exec(code, module.__dict__)
            # 제출 원본을 모듈에 보관하면 채점기가 메모리 모듈의 출력/주석을 검사할 수 있습니다.
            module.__source__ = code
            sys.modules[module_name] = module
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            result = f"❌ 제출 코드 실행 중 에러 발생:<br><pre>{e}\n\n{tb}</pre>"
            return render_template_string(HTML, problem=PROBLEM, result=result)

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
            with contextlib.redirect_stdout(buf):
                # 이미 임포트되어 있을 수 있으므로 reload로 최신 상태 반영
                if 'test_checker' in sys.modules:
                    importlib.reload(sys.modules['test_checker']).run_week(week)
                else:
                    import test_checker
                    importlib.reload(test_checker)
                    test_checker.run_week(week)
            output = buf.getvalue()
            result = f"<b>자동 채점 결과:</b><br><pre>{output}</pre><br>✅ 정상 실행!"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            output = f"{e}\n\n{tb}"
            result = f"❌ 자동 채점 중 에러 발생:<br><pre>{output}</pre>"

        # GitHub 이슈 생성
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
                result += "<br>✅ GitHub 이슈가 성공적으로 생성되었습니다!"
            else:
                result += f"<br>❌ GitHub 이슈 생성 실패: {r.text}"
        else:
            result += "<br>⚠️ GitHub 토큰이 설정되어 있지 않습니다."

    # 렌더링 결과 반환
    return render_template_string(HTML, problem=PROBLEM, result=result)

# 로컬에서는 5555, Vercel에서는 자동 포트로 동작
# 로컬 푸시할때는 vercel 환경에서 실행 안되니 주석처리
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5555))
#     app.run(port=port)