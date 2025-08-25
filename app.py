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
        # 제출 코드를 파일로 저장
    with open("week1_variable.py", "w", encoding="utf-8") as f:
        f.write(code)
    # test_checker.py 실행
    import subprocess
    try:
        output = subprocess.check_output(
            [sys.executable, "test_checker.py"],
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        result = f"<b>자동 채점 결과:</b><br><pre>{output}</pre><br>✅ 정상 실행!"
    except Exception as e:
        output = str(e)
        result = f"❌ 자동 채점 중 에러 발생: {e}"

    # GitHub 이슈 생성
    if GITHUB_TOKEN:
        issue_title = f"[1주차] {username} 답안 제출"
        issue_body = f"**이름:** {username}\n\n**답안 코드:**\n```python\n{code}\n```\n\n**자동 채점 결과:**\n```\n{output}\n```"
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

# 로컬에서는 5555, Vercel에서는 자동 포트로 동작
# 로컬 푸시할때는 vercel 환경에서 실행 안되니 주석처리
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5555))
#     app.run(port=port)