import os
import requests
from flask import Flask, render_template_string, request
import io
import sys

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # 환경변수로 토큰 관리
GITHUB_REPO = "reomoon/study_python"

app = Flask(__name__)

PROBLEM = """
<h3>1주차: 변수 문제</h3>
<ol>
  <li>변수 x에 7을 저장하고, x의 값을 출력하세요.</li>
  <li>변수 a와 b에 각각 3과 8을 저장한 뒤, 두 변수의 곱을 출력하세요.</li>
  <li>변수 name에 자신의 이름을 저장하고, "내 이름은 OOO입니다."를 출력하세요.</li>
  <li>변수 width와 height에 각각 5와 10을 저장하고, 사각형의 넓이(가로*세로)를 출력하세요.</li>
  <li>변수 temp에 36.5를 저장하고, "현재 체온은 36.5도입니다."와 같이 출력하세요.</li>
</ol>
"""

HTML = '''
<h2>Python 기초 스터디 자동 채점기</h2>
<div style="background:#f8f9fa;padding:15px;border-radius:10px;margin-bottom:20px;">{{ problem|safe }}</div>
<form method="post" onsubmit="document.getElementById('code').value = editor.getValue();">
    이름: <input name="username" required><br><br>
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
        # 코드 실행 결과 캡처
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            exec(code)
            output = mystdout.getvalue()
            result = f"<b>출력 결과:</b><br><pre>{output}</pre><br>✅ 정상 실행!"
        except Exception as e:
            result = f"❌ 에러 발생: {e}"
        finally:
            sys.stdout = old_stdout
        # GitHub 이슈 생성
        if GITHUB_TOKEN:
            issue_title = f"[1주차] {username} 답안 제출"
            issue_body = f"**이름:** {username}\n\n**답안 코드:**\n```python\n{code}\n```\n\n**실행 결과:**\n{output if 'output' in locals() else result}"
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
    return render_template_string(HTML, result=result, problem=PROBLEM)

