# Week 6 example: 함수/모듈
def add(a, b):
    """Return sum of two numbers"""
    return a + b

print(add(2, 3))

def reverse(s):
    """Return reversed string"""
    return s[::-1]

print(reverse('abc'))

# default arg
def greet(name='학생'):
    return f'안녕하세요, {name}'

print(greet())

# 리스트에서 최대값 반환

def find_max(lst):
    return max(lst)
print(find_max([1, 5, 3, 9, 2]))

# 소수 판별

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
print(is_prime(7))
print(is_prime(8))

# 리스트에서 특정 값 개수 세기

def count_value(lst, value):
    return lst.count(value)
print(count_value([1, 2, 2, 3, 2], 2))
