# generators.py

# 1. Генератор квадратов до N
def generate_squares(n):
    for i in range(n + 1):
        yield i ** 2


# 2. Генератор чётных чисел от 0 до n
def generate_even(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i


# 3. Генератор чисел, делящихся на 3 и 4 (то есть на 12)
def generate_divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i


# 4. Генератор квадратов от a до b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


# 5. Генератор от n до 0
def generate_reverse(n):
    for i in range(n, -1, -1):
        yield i


# Пример запуска
if __name__ == "__main__":
    print("Squares up to 5:")
    for num in generate_squares(5):
        print(num)

    print("\nEven numbers up to 10:")
    print(",".join(str(x) for x in generate_even(10)))

    print("\nDivisible by 3 and 4 up to 50:")
    for num in generate_divisible_by_3_and_4(50):
        print(num)

    print("\nSquares from 3 to 6:")
    for num in squares(3, 6):
        print(num)

    print("\nReverse from 5 to 0:")
    for num in generate_reverse(5):
        print(num)
