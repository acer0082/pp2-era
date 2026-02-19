class University:
    # Переменная класса
    university_name = "KBTU"

    def __init__(self, student_name):
        self.student_name = student_name


student1 = University("Erasyl")
student2 = University("Dias")

print(student1.student_name, "-", student1.university_name)
print(student2.student_name, "-", student2.university_name)
