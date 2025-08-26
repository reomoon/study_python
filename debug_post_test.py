from app import app

client = app.test_client()

# Load an example code (if available)
try:
    from examples.week1_example import __doc__ as _dummy
    with open('examples/week1_example.py', 'r', encoding='utf-8') as f:
        example = f.read()
except Exception:
    example = "# sample\nx = 7\nprint('x =', x)\n"

data = {
    'username': 'Tester',
    'week': '1',
    'stdin': '',
    'code': example,
}

print('Posting form with fields:', list(data.keys()))
resp = client.post('/', data=data)
print('Status:', resp.status_code)
print('Response length:', len(resp.data))
print('Response preview:\n')
print(resp.data.decode('utf-8', errors='replace')[:2000])

# Also try a request missing username to check 400 behavior
print('\n--- Posting without username to check 400 behavior ---')
bad = dict(data)
del bad['username']
resp2 = client.post('/', data=bad)
print('Status (missing username):', resp2.status_code)
print(resp2.data.decode('utf-8', errors='replace')[:1000])
