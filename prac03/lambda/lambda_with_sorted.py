students = [
    {"name": "Erasyl", "grade": 85},
    {"name": "Aruzhan", "grade": 92},
    {"name": "Dias", "grade": 78}
]

# Сортировка по оценке
sorted_students = sorted(students, key=lambda student: student["grade"])

print("Sorted by grade:")
for student in sorted_students:
    print(student)
