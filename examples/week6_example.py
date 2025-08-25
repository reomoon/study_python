# Week 6 example: 함수/모듈
def add(a,b):
    """Return sum of two numbers"""
    return a + b

print(add(2,3))

def reverse(s):
    """Return reversed string"""
    return s[::-1]

print(reverse('abc'))

# default arg
def greet(name='학생'):
    return f'안녕하세요, {name}'

print(greet())
