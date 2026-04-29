-- 1. Поиск по паттерну (часть имени или телефона)
CREATE OR REPLACE FUNCTION search_by_pattern(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone
        FROM phonebook c
        WHERE c.name  ILIKE '%' || p || '%'
           OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Пагинация (получить записи порциями)
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone
        FROM phonebook c
        ORDER BY c.id
        LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;