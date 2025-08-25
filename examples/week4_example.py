# Week 4 example: 조건문/예외처리
n = 5
if n % 2 == 0:
    print('짝수')
else:
    print('홀수')

s = '10'
try:
    v = int(s)
    if v == 0:
        print('영')
    elif v > 0:
        print('양수')
    else:
        print('음수')
except ValueError:
    print('입력 오류')

try:
    x = int('notint')
except Exception as e:
    print('예외 발생:', e)
