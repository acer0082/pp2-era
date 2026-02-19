# Использование *args
def sum_all(*args):
    # Принимает любое количество чисел и возвращает их сумму
    total = sum(args)
    return total


# Использование **kwargs
def print_user_info(**kwargs):
    # Выводит информацию в формате ключ-значение
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print("Sum:", sum_all(1, 2, 3, 4, 5))

print_user_info(name="Erasyl", major="Information Systems", university="KBTU")
