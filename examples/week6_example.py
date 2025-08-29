# Week 6 example: 함수/모듈
def add(a, b):
    """Return sum of two numbers"""
    return a + b

print(add(2, 3))

def reverse(s):
    """Return reversed string"""
    return s[::-1]

print(reverse('abc'))

# 구구단 모듈 import해서 3단 실행 예시
from gugudan import print_gugudan
print_gugudan(3)

# default arg
def greet(name='학생'):
    return f'안녕하세요, {name}'

print(greet())
