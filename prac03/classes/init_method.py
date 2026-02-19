# Класс с конструктором
class Student:
    def __init__(self, name, major):
        # Инициализация атрибутов
        self.name = name
        self.major = major

    def introduce(self):
        print(f"My name is {self.name} and I study {self.major}.")


student = Student("Erasyl", "Information Systems")
student.introduce()
