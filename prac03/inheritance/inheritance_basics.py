# Базовый класс
class Animal:
    def speak(self):
        print("The animal makes a sound")


# Дочерний класс
class Dog(Animal):
    def bark(self):
        print("The dog barks")


dog = Dog()
dog.speak()
dog.bark()
