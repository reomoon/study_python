import pathlib
import app as app_module

def main():
    app = app_module.app
    app.testing = True
    client = app.test_client()

    # Use week2 example as submission to reproduce the reported issue
    ex_path = pathlib.Path('examples/week2_example.py')
    if not ex_path.exists():
        print('examples/week2_example.py not found')
        return
    code = ex_path.read_text(encoding='utf-8')

    data = {
        'username': 'tester',
        'week': '2',
        'stdin': '',
        'code': code,
    }

    resp = client.post('/', data=data)
    print('HTTP', resp.status_code)
    text = resp.get_data(as_text=True)
    # Print a trimmed response for inspection
    print('\n--- Response excerpt (first 4000 chars) ---\n')
    print(text[:4000])
    # Try to extract checker output section
    if '채점기 출력' in text or '자동 채점 결과' in text:
        print('\n[채점 결과가 응답에 포함되어 있습니다]')
    else:
        print('\n[채점 결과가 응답에 없습니다]')

if __name__ == '__main__':
    main()
