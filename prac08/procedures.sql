-- 1. Upsert: добавить контакт или обновить телефон если имя уже есть
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
        RAISE NOTICE 'Обновлён: %', p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
        RAISE NOTICE 'Добавлен: %', p_name;
    END IF;
END;
$$;


-- 2. Bulk insert: добавить много контактов, валидация телефона
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[],
    OUT invalid_data TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    invalid TEXT := '';
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        -- Валидация: телефон должен начинаться с + и содержать только цифры
        IF p_phones[i] !~ '^\+[0-9]{10,15}$' THEN
            invalid := invalid || p_names[i] || ':' || p_phones[i] || '; ';
        ELSE
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
                UPDATE phonebook SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i]);
            END IF;
        END IF;
    END LOOP;
    invalid_data := invalid;
END;
$$;


-- 3. Удалить по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_type = 'name' THEN
        DELETE FROM phonebook WHERE name = p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_value;
    ELSE
        RAISE EXCEPTION 'p_type должен быть "name" или "phone"';
    END IF;
END;
$$;