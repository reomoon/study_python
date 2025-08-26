import pathlib
import re
import app as app_module

def extract_sections(html):
    # student_output: first <pre> after '결과:'
    student = ''
    checker = ''
    m = re.search(r"<b>결과:</b>.*?(<pre>.*?</pre>)", html, flags=re.S)
    if m:
        student = re.sub(r'<.*?>', '', m.group(1)).strip()
    m2 = re.search(r"<h4>채점기 출력</h4>\s*<pre>(.*?)</pre>", html, flags=re.S)
    if m2:
        checker = m2.group(1).strip()
    return student, checker

def main():
    app = app_module.app
    app.testing = True
    client = app.test_client()

    ex_path = pathlib.Path('examples/week1_example.py')
    if not ex_path.exists():
        print('examples/week1_example.py not found')
        return
    code = ex_path.read_text(encoding='utf-8')

    data = {
        'username': 'tester',
        'week': '1',
        'stdin': '',
        'code': code,
    }

    resp = client.post('/', data=data)
    print('HTTP', resp.status_code)
    html = resp.get_data(as_text=True)
    student, checker = extract_sections(html)
    print('\n=== STUDENT OUTPUT ===\n')
    print(student or '(없음)')
    print('\n=== CHECKER OUTPUT ===\n')
    print(checker or '(없음)')

if __name__ == '__main__':
    main()
