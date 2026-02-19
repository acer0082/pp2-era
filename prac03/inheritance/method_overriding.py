class Animal:
    def speak(self):
        print("Some generic animal sound")


class Cat(Animal):
    # Переопределение метода
    def speak(self):
        print("Meow")


cat = Cat()
cat.speak()
