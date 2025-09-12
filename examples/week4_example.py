# Week 4 example: 조건문/예외처리

# 1. 숫자 하나를 변수에 넣고, 짝수/홀수 출력
num = 7
if num % 2 == 0:
    print("짝수")
else:
    print("홀수")

# 2. 입력값이 0이면 "영", 음수면 "음수", 양수면 "양수" 출력
n = int(input())
if n == 0:
    print("영")
elif n < 0:
    print("음수")
else:
    print("양수")

# 3. 문자열을 정수로 변환, 예외 발생 시 "입력 오류" 출력
s = input()
try:
    val = int(s)
    print(val)
except ValueError:
    print("입력 오류")

# 4. 입력값이 10보다 큰지 확인
num = int(input())
if num > 10:
    print(f"입력한 {num}값이 10보다 큽니다.")
elif num < 10:
    print(f"입력한 {num}값이 10보다 작습니다.")
elif num == 10:
    print("입력한 값은 10 입니다.")
else:
    print("잘못 입력 하였습니다.")

# 5. 강제로 에러 발생시키고 예외로 잡기
try:
    raise Exception("강제 에러 발생!")
except Exception as e:
    print(f"에러 잡음: {e}")
