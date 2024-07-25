------
CREATE OR REPLACE FUNCTION Учёт.before_delete_departmentposition_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF (SELECT COUNT(*) FROM Учёт.Работники WHERE Позиция=OLD."Номер позиции") > 0 THEN
		UPDATE Учёт.Работники
		SET Позиция = NULL
		WHERE Позиция=OLD."Номер позиции";
	END IF;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER delete_departmentposition_trigger
BEFORE DELETE ON Учёт."Должность-Отдел"
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_delete_departmentposition_function();
------
CREATE OR REPLACE FUNCTION Учёт.before_delete_positions_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF (SELECT COUNT(*) FROM Учёт."Должность-Отдел" WHERE Должность = OLD."Номер должности") > 0 THEN
		DELETE FROM Учёт."Должность-Отдел" WHERE Должность=OLD."Номер должности";
	END IF;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER delete_positions_trigger
BEFORE DELETE ON Учёт.Должности
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_delete_positions_function();
------
CREATE OR REPLACE FUNCTION Учёт.before_delete_departments_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF (SELECT COUNT(*) FROM Учёт."Должность-Отдел" WHERE Отдел=OLD."Номер отдела") > 0 THEN
		DELETE FROM Учёт."Должность-Отдел" WHERE Отдел=OLD."Номер отдела";
	END IF;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER delete_departments_trigger
BEFORE DELETE ON Учёт.Отделы
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_delete_departments_function();
------
CREATE OR REPLACE FUNCTION Учёт.before_delete_workers_function()
RETURNS TRIGGER AS
$$
BEGIN
	IF (SELECT COUNT(*) FROM Учёт.Аутентификации WHERE Работник=OLD."Табельный номер") > 0 THEN
		DELETE FROM Учёт.Аутентификации WHERE Работник=OLD."Табельный номер";
	END IF;
	IF (SELECT COUNT(*) FROM Учёт.Смены WHERE "Табельный номер"=OLD."Табельный номер") > 0 THEN
		DELETE FROM Учёт.Смены WHERE "Табельный номер"=OLD."Табельный номер";
	END IF;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';
CREATE TRIGGER delete_workers_trigger
BEFORE DELETE ON Учёт.Работники
FOR EACH ROW
EXECUTE FUNCTION Учёт.before_delete_workers_function();
------
/*
SELECT * FROM information_schema.triggers WHERE trigger_schema='Учёт' AND trigger_name LIKE 'no_%';
*/