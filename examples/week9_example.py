import os

# Week 9 example: 파일 입출력
# 1. 텍스트 파일 생성 및 저장
fn = 'examples_week9.txt'
with open(fn, 'w', encoding='utf-8') as f:
    f.write('line1\nline2\n')

# 2. 저장한 파일 열어서 내용 읽고 출력
with open(fn, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 3. 파일 없을 때 예외 처리
try:
    with open('not_exist.txt', 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print('파일이 없습니다.')

# 4. 각 줄을 리스트에 저장하고 길이 출력
with open(fn, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(lines)
    print(len(lines))

# 5. 파일에 덧붙이기(append) 모드로 한 줄 추가
with open(fn, 'a', encoding='utf-8') as f:
    f.write('line3\n')

os.remove(fn)  # cleanup
