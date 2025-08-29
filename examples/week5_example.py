# Week 5 example: 반복문
for i in range(1,6):
    print(i)

numbers = [1,2,3,4]
print(sum(numbers))

# 3. while문 카운트다운
n = 3
while n >= 0:
    print(n)
    n -= 1

# 4. 리스트 컴프리헨션
squares = [x*x for x in range(1, 6)]
print(squares)

# 5. for문 구구단
for i in range(2, 10):
    for j in range(1, 10):
        print(f"{i} x {j} = {i*j}")

