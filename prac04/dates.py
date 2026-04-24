# dates.py

from datetime import datetime, timedelta

# 1. Вычесть 5 дней от текущей даты
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Five days ago:", five_days_ago)

# 2. Вчера, сегодня, завтра
yesterday = current_date - timedelta(days=1)
tomorrow = current_date + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", current_date)
print("Tomorrow:", tomorrow)

# 3. Убрать микросекунды
without_microseconds = current_date.replace(microsecond=0)
print("Without microseconds:", without_microseconds)

# 4. Разница двух дат в секундах
date1 = datetime(2026, 2, 10, 12, 0, 0)
date2 = datetime(2026, 2, 15, 12, 0, 0)

difference = abs((date2 - date1).total_seconds())
print("Difference in seconds:", difference)
