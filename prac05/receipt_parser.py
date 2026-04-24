import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = [line.strip() for line in re.split(r"\r?\n", text) if line.strip()]

products = []
prices = []

i = 0
while i < len(lines):

    # ищем номер товара
    if re.match(r"^\d+\.$", lines[i]):

        if i + 3 < len(lines):

            product = lines[i + 1]
            price_line = lines[i + 3]

            match = re.search(r"\d[\d\s]*,\d{2}", price_line)

            if match:
                price = float(match.group().replace(" ", "").replace(",", "."))
                products.append(product)
                prices.append(price)

        i += 4
    else:
        i += 1

# дата и время
dt = re.search(r"(\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})", text)
date, time = (dt.groups() if dt else (None, None))

# оплата
payment = re.search(r"Банковская карта|Наличные", text)
payment = payment.group() if payment else None

# итог
total_match = re.search(r"ИТОГО:\s*([\d\s]+,\d{2})", text)
total = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else 0

result = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment": payment
}

print(json.dumps(result, indent=4, ensure_ascii=False))