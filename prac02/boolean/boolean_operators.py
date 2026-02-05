# Boolean operators
# and, or, not

age = 20
has_id = True

# and — оба условия должны быть True
if age >= 18 and has_id:
    print("Access granted")
else:
    print("Access denied")

# or — достаточно одного True
is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("You can rest")
else:
    print("Go to work")

# not — инверсия
is_raining = False

if not is_raining:
    print("Go for a walk")
else:
    print("Stay at home")

# Комбинация операторов
score = 85
passed = score >= 60 and score <= 100

print(passed)   # True
