class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, major):
        # Вызов конструктора родителя
        super().__init__(name)
        self.major = major

    def introduce(self):
        print(f"My name is {self.name} and I study {self.major}.")


student = Student("Erasyl", "Information Systems")
student.introduce()
