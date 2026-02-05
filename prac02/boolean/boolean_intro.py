
# Boolean — это тип данных с двумя значениями: True и False

is_student = True
is_employed = False

print(is_student)     # True
print(is_employed)    # False

# Boolean часто получается из условий
age = 18
is_adult = age >= 18

print(is_adult)       # True

# Boolean в if
if is_adult:
    print("You are an adult")
else:
    print("You are not an adult")
