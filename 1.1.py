j = input("Введите первые камни:")
s = input("Введите другие камни:")

count = 0
for char in s:
    if char in j:
        count += 1

print(f"Оказывается {count} из них не просто камни")