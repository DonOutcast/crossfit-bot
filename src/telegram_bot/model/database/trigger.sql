--DROP TRIGGER IF EXISTS trigger_handle_user_calendar_date ON calendar_date;
--DROP FUNCTION IF EXISTS handle_user_calendar_date() CASCADE;
--
--CREATE FUNCTION handle_user_calendar_date()
--    RETURNS TRIGGER AS $$
--    DECLARE
--        rec RECORD;
--        user_id INTEGER
--BEGIN
----    FOR rec IN SELECT * FROM new_table LOOP
----        RAISE NOTICE '%', rec;
----    END LOOP;
----    SELECT id INTO user_id FROM user
----    ORDER BY LIMIT 1;
--
--    CASE TG_OP
--        WHEN 'INSERT' THEN
--            INSERT INTO user_calendar_date(user_id, date_id)
--            VALUES (user_id, NEW.date_id);
--        WHEN 'UPDATE' THEN
--            UPDATE user_calendar_date
--            SET user_id = NEW.id, date_id = NEW.date_id
--            WHERE user_id = OLD.id AND date_id = OLD.date_id;
--        WHEN 'DELETE' THEN
--            DELETE FROM user_calendar_date
--            WHERE user_id = OLD.id AND date_id = OLD.date_id;
--   END CASE;
--    RETURN NULL;
--END;
--$$ LANGUAGE plpgsql;
--
--CREATE TRIGGER trigger_handle_user_calendar_date
--AFTER INSERT OR  ON calendar_date
----REFERENCING
----    NEW TABLE AS new_table
--FOR EACH ROW
--EXECUTE FUNCTION handle_user_calendar_date();


-- Создание таблицы users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(70) UNIQUE
);

-- Создание таблицы calendar_dates
CREATE TABLE calendar_dates (
    date_id SERIAL PRIMARY KEY,
    choice_date DATE
);

-- Создание таблицы user_calendar_dates как связующей таблицы
CREATE TABLE user_calendar_dates (
    user_id INTEGER REFERENCES users(user_id),
    date_id INTEGER REFERENCES calendar_dates(date_id),
    PRIMARY KEY (user_id, date_id)
);

-- Создание триггера для автоматического заполнения связующей таблицы
CREATE OR REPLACE FUNCTION handle_user_calendar_dates()
    RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_calendar_dates (user_id, date_id)
        VALUES ((SELECT user_id FROM users WHERE ), NEW.date_id);
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE user_calendar_dates
        SET date_id = NEW.date_id
        WHERE date_id = OLD.date_id;
    ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM user_calendar_dates
        WHERE date_id = OLD.date_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера после вставки или удаления в таблицу calendar_dates
CREATE TRIGGER trigger_calendar_dates
AFTER INSERT OR DELETE ON calendar_dates
FOR EACH ROW
EXECUTE FUNCTION handle_user_calendar_dates();