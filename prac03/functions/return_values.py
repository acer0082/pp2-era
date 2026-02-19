# Функция с возвращаемым значением
def add_numbers(a, b):
    # Возвращает сумму двух чисел
    return a + b


def is_even(number):
    # Проверяет, является ли число чётным
    return number % 2 == 0


sum_result = add_numbers(10, 5)
print("Sum:", sum_result)

print("Is 4 even?", is_even(4))
print("Is 7 even?", is_even(7))
