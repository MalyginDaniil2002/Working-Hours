------
CREATE OR REPLACE FUNCTION Учёт.before_update_positiondepartment_function()
RETURNS TRIGGER AS
$$
BEGIN
	RETURN NULL;
END
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER no_update_positiondepartment_trigger
BEFORE UPDATE ON Учёт."Должность-Отдел"
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_update_positiondepartment_function();
------
CREATE OR REPLACE FUNCTION Учёт.before_update_auth_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF NEW.Работник = OLD.Работник THEN
		RETURN NULL;
	END IF;
	RETURN NEW;
END
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER no_update_auth_trigger
BEFORE UPDATE ON Учёт.Аутентификации
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_update_auth_function();
------
CREATE OR REPLACE FUNCTION Учёт.after_update_shifts_function()
RETURNS TRIGGER AS
$$
DECLARE
	new_number integer;
	start_point interval;
	end_point interval;
	multiplier numeric;
	salary numeric;
BEGIN
	IF (NEW.Замечания = OLD.Замечания) AND (OLD.Зарплата = NEW.Зарплата)
	AND (OLD."Дата смены" = NEW."Дата смены") AND (OLD."Время работы" = NEW."Время работы")  AND
	(OLD."Временные точки" <> NEW."Временные точки") THEN
		new_number = NEW."Номер смены";
		start_point = NEW."Начало смены";
		end_point = NEW."Окончание смены";
		IF (OLD."Начало смены" <> start_point) OR (OLD."Окончание смены" <> end_point) THEN
			UPDATE Учёт.Смены
			SET "Время работы"=end_point - start_point
			WHERE "Номер смены"=new_number;
		END IF;
		multiplier = (
			SELECT "Текущий оклад"
			FROM Учёт.Работники
			WHERE "Табельный номер" = (
				SELECT "Табельный номер"
				FROM Учёт.Смены
				WHERE "Номер смены"=NEW."Номер смены"
			)
		);
		salary = multiplier * EXTRACT(epoch FROM (end_point - start_point)::interval)/3600;
		UPDATE Учёт.Смены
		SET Зарплата=salary
		WHERE "Номер смены"=new_number;
	END IF;
	RETURN NEW;
END
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER update_shifts_trigger
AFTER UPDATE ON Учёт.Смены
FOR EACH ROW
EXECUTE FUNCTION Учёт.after_update_shifts_function();
------
CREATE OR REPLACE FUNCTION Учёт.before_update_workers_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF NEW."Табельный номер" <> OLD."Табельный номер" THEN
		UPDATE Учёт.Аутентификации SET Работник = NULL WHERE Работник = OLD."Табельный номер";
		UPDATE Учёт.Смены SET "Табельный номер" = NULL WHERE "Табельный номер" = OLD."Табельный номер";
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER before_update_workers_trigger
BEFORE UPDATE ON Учёт.Работники
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_update_workers_function();
------
CREATE OR REPLACE FUNCTION Учёт.after_update_workers_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF NEW."Табельный номер" <> OLD."Табельный номер" THEN
		UPDATE Учёт.Аутентификации
		SET Работник = NEW."Табельный номер"
		WHERE Работник isnull;
		UPDATE Учёт.Смены
		SET "Табельный номер" = NEW."Табельный номер"
		WHERE "Табельный номер" isnull;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER after_update_workers_trigger
AFTER UPDATE ON Учёт.Работники
FOR EACH ROW
EXECUTE FUNCTION Учёт.after_update_workers_function();
------
/*
SELECT * FROM information_schema.triggers WHERE trigger_schema='Учёт' AND trigger_name LIKE 'no_%';
*/