# Week 5 example: 반복문
for i in range(1,6):
    print(i)

numbers = [1,2,3,4]
print(sum(numbers))

# while countdown
n = 3
while n >= 0:
    print(n)
    n -= 1

squares = [i*i for i in range(5)]
print(squares)

for x in [0,1,2,3]:
    if x == 2:
        continue
    print(x)
