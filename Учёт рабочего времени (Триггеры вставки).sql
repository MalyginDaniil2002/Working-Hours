------
CREATE OR REPLACE FUNCTION Учёт.after_insert_workers_function()
RETURNS TRIGGER AS
$$
DECLARE
	salary numeric;
BEGIN
	salary = (
		SELECT "Начальный оклад"
		FROM Учёт."Должность-Отдел", Учёт.Должности
		WHERE Должность = "Номер должности" AND "Номер позиции" = (
			SELECT Позиция
			FROM Учёт.Работники
			WHERE "Табельный номер" = NEW."Табельный номер"
		)
	);
	UPDATE Учёт.Работники
	SET "Текущий оклад" = salary
	WHERE "Табельный номер" = NEW."Табельный номер";
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER insert_workers_trigger
AFTER INSERT ON Учёт.Работники
FOR EACH ROW
EXECUTE FUNCTION Учёт.after_insert_workers_function();
------
CREATE OR REPLACE FUNCTION Учёт.insert_auth_function()
RETURNS TRIGGER AS
$$
DECLARE
	login varchar;
	max_length integer;
	password varchar;
BEGIN
	login = NEW.Телефон;
	max_length = (
		select character_maximum_length
		from INFORMATION_SCHEMA.COLUMNS
		where column_name = 'Пароль'
	);
	password=(SELECT SUBSTR(MD5(RANDOM()::text), 1, max_length));
	WHILE (SELECT COUNT(*) FROM Учёт.Аутентификации WHERE Логин=login AND Пароль=password) > 0 LOOP
		password=(SELECT SUBSTR(MD5(RANDOM()::text), 1, max_length));
	END LOOP;
	INSERT INTO Учёт.Аутентификации(Работник, Логин, Пароль) VALUES (NEW."Табельный номер", login, password);
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER insert_auth_trigger
AFTER INSERT ON Учёт.Работники
FOR EACH ROW
EXECUTE FUNCTION Учёт.insert_auth_function();
------
CREATE OR REPLACE FUNCTION Учёт.after_insert_shifts_function()
RETURNS TRIGGER AS
$$
DECLARE
	index integer;
	diff interval;
	new_data json;
BEGIN
	index = 0;
	diff=NEW."Окончание смены"-NEW."Начало смены";
	new_data = (SELECT '{}'::jsonb);
	WHILE index < 24 LOOP
		new_data = jsonb_insert(new_data::jsonb, CAST(CONCAT('{', CONCAT((index::text), 'H')::interval, '}') AS text[]), 'false');
		index = index + 1;
	END LOOP;
	UPDATE Учёт.Смены
	SET "Время работы"=diff, "Временные точки"=new_data
	WHERE "Номер смены"=NEW."Номер смены";
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER insert_shifts_trigger
AFTER INSERT ON Учёт.Смены
FOR EACH ROW
EXECUTE FUNCTION Учёт.after_insert_shifts_function();
------
/*
SELECT * FROM information_schema.triggers WHERE trigger_schema='Учёт' AND trigger_name LIKE 'no_%';
*/