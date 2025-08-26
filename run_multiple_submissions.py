import pathlib
import app as app_module

def submit_example(client, week):
    ex_path = pathlib.Path(f'examples/week{week}_example.py')
    if not ex_path.exists():
        print(f'week{week} 예제 없음 — 스킵')
        return
    code = ex_path.read_text(encoding='utf-8')
    data = {
        'username': 'tester',
        'week': str(week),
        'stdin': '',
        'code': code,
    }
    resp = client.post('/', data=data)
    text = resp.get_data(as_text=True)
    has_checker = '채점기 출력' in text or '자동 채점 결과' in text
    print(f'주차 {week}: HTTP {resp.status_code}, 채점 결과 포함: {has_checker}')

def main():
    app = app_module.app
    app.testing = True
    client = app.test_client()
    for w in [1,2,3]:
        submit_example(client, w)

if __name__ == '__main__':
    main()
