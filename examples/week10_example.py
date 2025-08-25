# Week 10 example: 클래스
class Person:
    """간단한 사람 클래스"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"안녕하세요, 제 이름은 {self.name}입니다"

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

p = Person('홍길동', 30)
print(p.greet())
s = Student('학생', 20, 'Seoul High')
print(s)
