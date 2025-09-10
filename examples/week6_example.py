# Week 6 example: 함수/모듈

#1
def add(a, b):
    print(a + b)

add(2, 3)

#2
def reverse(s):
    return s[::-1]

result = reverse('hello')
print(result)

# 3 : default arg
def greet(name='학생'):
    return f'안녕하세요, {name}'

print(greet())

# 4 : 함수 내부에 문자열 작성해서 __doc__ 채우기
def greet(name='학생'):
    """이름을 입력받아 환영 메시지를 출력하는 함수입니다."""
    print(f"안녕하세요, {name}님!")

greet()

# 5 : 리스트에서 최대값 반환
def find_max(lst):
    return max(lst)
print(find_max([1, 5, 3, 9, 2]))

# 6 : 소수 판별
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(7))
print(is_prime(8))

# 7 : 리스트에서 특정 값의 개수 세기
def count_value(lst, value):
    return lst.count(value)

print(count_value([1, 2, 2, 3], 2))
