from connect import get_connection

def create_table():
    conn = get_connection()
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

# ─── Поиск по паттерну ──────────────────────────────────────────
def search_by_pattern():
    pattern = input("Введи часть имени или телефона: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_by_pattern(%s);", (pattern,))
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

# ─── Upsert (добавить или обновить) ─────────────────────────────
def upsert_contact():
    name  = input("Имя: ")
    phone = input("Телефон: ")
    conn  = get_connection()
    cur   = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    print("Готово.")
    cur.close()
    conn.close()

# ─── Bulk insert ─────────────────────────────────────────────────
def insert_many():
    print("Вводи контакты в формате  Имя,Телефон  (пустая строка = стоп)")
    names, phones = [], []
    while True:
        line = input(">> ")
        if not line:
            break
        parts = line.split(',')
        if len(parts) != 2:
            print("Неверный формат, пропускаю.")
            continue
        names.append(parts[0].strip())
        phones.append(parts[1].strip())

    if not names:
        print("Нет данных.")
        return

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "CALL insert_many_contacts(%s::VARCHAR[], %s::VARCHAR[], NULL);",
        (names, phones)
    )
    conn.commit()

    # Получить invalid_data из OUT параметра
    cur.execute(
        "SELECT invalid_data FROM insert_many_contacts(%s::VARCHAR[], %s::VARCHAR[], NULL) AS t(invalid_data);",
        (names, phones)
    )
    # Вызываем функцию чтобы получить invalid_data
    cur.execute("""
        DO $$
        DECLARE
            inv TEXT;
        BEGIN
            CALL insert_many_contacts(%s::VARCHAR[], %s::VARCHAR[], inv);
            RAISE NOTICE 'Invalid: %', inv;
        END;
        $$;
    """, (names, phones))
    conn.commit()
    print("Загрузка завершена. Проверь консоль на наличие невалидных данных.")
    cur.close()
    conn.close()

# ─── Пагинация ───────────────────────────────────────────────────
def show_paginated():
    limit  = int(input("Сколько записей на странице: "))
    page   = int(input("Номер страницы (с 1): "))
    offset = (page - 1) * limit
    conn   = get_connection()
    cur    = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    if rows:
        print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
    else:
        print("Нет данных на этой странице.")
    cur.close()
    conn.close()

# ─── Удалить контакт ─────────────────────────────────────────────
def delete_contact():
    print("Удалить по:  1 - Имени  2 - Телефону")
    choice = input("Выбор: ")
    value  = input("Значение: ")
    kind   = 'name' if choice == '1' else 'phone'
    conn   = get_connection()
    cur    = conn.cursor()
    cur.execute("CALL delete_contact(%s, %s);", (value, kind))
    conn.commit()
    print("Удалено.")
    cur.close()
    conn.close()

# ─── Меню ────────────────────────────────────────────────────────
def main():
    create_table()
    while True:
        print("\n=== PhoneBook (Practice 8) ===")
        print("1 - Поиск по паттерну")
        print("2 - Добавить / обновить контакт (upsert)")
        print("3 - Добавить много контактов")
        print("4 - Просмотр с пагинацией")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")
        if   choice == '1': search_by_pattern()
        elif choice == '2': upsert_contact()
        elif choice == '3': insert_many()
        elif choice == '4': show_paginated()
        elif choice == '5': delete_contact()
        elif choice == '0': break
        else: print("Неверный выбор.")

if __name__ == "__main__":
    main()