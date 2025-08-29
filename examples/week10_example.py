# Week 10 example: 클래스
class Person:
    """간단한 사람 클래스"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"안녕하세요, 제 이름은 {self.name}입니다"

    def __str__(self):
        return f"{self.name}({self.age})"

class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def __str__(self):
        return f"{self.name}({self.age}) - {self.school}"

class Classroom:
    def __init__(self):
        self.students = []
    def add_student(self, student):
        self.students.append(student)
    def show_students(self):
        for s in self.students:
            print(s)

# 예시 사용
c = Classroom()
c.add_student(Student("은우", 17, "서울고"))
c.add_student(Student("원영", 16, "서울여고"))
c.show_students()

p = Person('홍길동', 30)
print(p.greet())
s = Student('학생', 20, 'Seoul SChool')
print(s)
