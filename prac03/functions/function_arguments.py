# Функция с несколькими аргументами
def introduce(name, age):
    # Вывод информации о человеке
    print(f"My name is {name} and I am {age} years old.")


# Аргументы по умолчанию
def power(base, exponent=2):
    # Возведение в степень
    result = base ** exponent
    print(f"{base} to the power of {exponent} is {result}")


introduce("Erasyl", 18)
power(5)
power(2, 3)
