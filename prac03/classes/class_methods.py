class Calculator:
    # Обычный метод
    def add(self, a, b):
        return a + b

    # Статический метод
    @staticmethod
    def multiply(a, b):
        return a * b


calc = Calculator()
print("Addition:", calc.add(5, 3))
print("Multiplication:", Calculator.multiply(4, 2))
