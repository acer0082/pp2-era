import csv
from connect import get_connection

# ─── Создание таблицы ───────────────────────────────────────────
def create_table():
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id    SERIAL PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            phone VARCHAR(20)  NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблица создана.")

# ─── Импорт из CSV ──────────────────────────────────────────────
def import_from_csv(filename):
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO phonebook (name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING;
            """, (row['name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()
    print("Данные из CSV импортированы.")

# ─── Добавить контакт вручную ───────────────────────────────────
def insert_from_console():
    name  = input("Имя: ")
    phone = input("Телефон: ")
    conn  = get_connection()
    if not conn: return
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO phonebook (name, phone)
            VALUES (%s, %s);
        """, (name, phone))
        conn.commit()
        print("Контакт добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    cur.close()
    conn.close()

# ─── Обновить контакт ───────────────────────────────────────────
def update_contact():
    print("Что обновить?")
    print("1 - Имя  2 - Телефон")
    choice = input("Выбор: ")
    old = input("Текущее значение (имя или телефон для поиска): ")
    new = input("Новое значение: ")
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    if choice == '1':
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s;", (new, old))
    else:
        cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s;", (new, old))
    conn.commit()
    print(f"Обновлено строк: {cur.rowcount}")
    cur.close()
    conn.close()

# ─── Поиск контактов ────────────────────────────────────────────
def search_contacts():
    print("Поиск по:  1 - Имени  2 - Префиксу телефона  3 - Все контакты")
    choice = input("Выбор: ")
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    if choice == '1':
        name = input("Имя (или часть): ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s;", (f'%{name}%',))
    elif choice == '2':
        prefix = input("Префикс телефона: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", (f'{prefix}%',))
    else:
        cur.execute("SELECT * FROM phonebook ORDER BY name;")
    rows = cur.fetchall()
    if rows:
        print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
    else:
        print("Ничего не найдено.")
    cur.close()
    conn.close()

# ─── Удалить контакт ────────────────────────────────────────────
def delete_contact():
    print("Удалить по:  1 - Имени  2 - Телефону")
    choice = input("Выбор: ")
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    if choice == '1':
        name = input("Имя: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s;", (name,))
    else:
        phone = input("Телефон: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s;", (phone,))
    conn.commit()
    print(f"Удалено строк: {cur.rowcount}")
    cur.close()
    conn.close()

# ─── Главное меню ───────────────────────────────────────────────
def main():
    create_table()
    while True:
        print("\n=== PhoneBook ===")
        print("1 - Импорт из CSV")
        print("2 - Добавить контакт")
        print("3 - Обновить контакт")
        print("4 - Поиск контактов")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")
        if   choice == '1': import_from_csv('contacts.csv')
        elif choice == '2': insert_from_console()
        elif choice == '3': update_contact()
        elif choice == '4': search_contacts()
        elif choice == '5': delete_contact()
        elif choice == '0': break
        else: print("Неверный выбор.")

if __name__ == "__main__":
    main()