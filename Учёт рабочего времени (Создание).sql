--Проектирование БД системы учёта рабочего времени на производстве.
/*REVOKE CONNECT ON DATABASE times FROM public;
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'times';
DROP DATABASE times;
CREATE DATABASE times;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
DROP SCHEMA Учёт CASCADE;
CREATE SCHEMA Учёт;
DROP TABLE Учёт.Отделы, Учёт.Должности, Учёт."Должность-Отдел";*/
CREATE TABLE Учёт.Должности
(
	"Номер должности" serial PRIMARY KEY,
	Название varchar,
	"Начальный оклад" numeric(10, 2) DEFAULT 0 CHECK ("Начальный оклад" >= 0)
);
CREATE TABLE Учёт.Отделы
(
	"Номер отдела" serial PRIMARY KEY,
	Название varchar
);
CREATE TABLE Учёт."Должность-Отдел"
(
	"Номер позиции" serial PRIMARY KEY,
	Отдел serial REFERENCES Учёт.Отделы("Номер отдела"),
	Должность serial REFERENCES Учёт.Должности("Номер должности")
);
CREATE TYPE Учёт."Типы занятости" AS ENUM
(
	'Полная занятость',
	'Неполная занятость',
	'Временная занятость',
	'Сезонная занятость',
	'Внештатная занятость',
	'Фриланс'
);
CREATE TABLE Учёт.Работники
(
	"Табельный номер" varchar(20) PRIMARY KEY,
	Фамилия varchar(50),
	Имя varchar(50),
	Отчество varchar(50),
	"Дата рождения" date CHECK ("Дата рождения" < current_date),
	Телефон varchar(16),
	Почта varchar,
	Позиция serial REFERENCES Учёт."Должность-Отдел"("Номер позиции"),
	"Тип занятости" Учёт."Типы занятости",
	"Дата найма" date DEFAULT current_date,
	"Текущий оклад" numeric(10, 2) DEFAULT 0 CHECK ("Текущий оклад" >= 0)
);
CREATE TABLE Учёт.Аутентификации
(
	Работник varchar(20) REFERENCES Учёт.Работники("Табельный номер"),
	Логин varchar(12),
	Пароль varchar(15),
	UNIQUE(Логин, Пароль)
);
CREATE TABLE Учёт.Смены
(
	"Номер смены" serial PRIMARY KEY,
	"Табельный номер" varchar(20) REFERENCES Учёт.Работники("Табельный номер"),
	"Дата смены" date CHECK ("Дата смены" >= NOW()::date),
	"Начало смены" interval,
	"Окончание смены" interval CHECK ("Окончание смены" > "Начало смены"),
	"Время работы" interval DEFAULT '0 hours',
	"Временные точки" jsonb,
	Замечания text[] DEFAULT '{}',
	Зарплата numeric(14, 2) DEFAULT 0
);
CREATE OR REPLACE VIEW Учёт."Данные о текущих работниках" AS
	SELECT "Табельный номер", Фамилия, Имя, Отчество, "Дата рождения",
	Телефон, Почта, Отделы.Название AS "Отдел", Должности.Название AS "Должность",
	"Тип занятости", "Дата найма", "Текущий оклад"
	FROM Учёт.Отделы, Учёт.Должности, Учёт."Должность-Отдел", Учёт.Работники
	WHERE Позиция="Номер позиции" AND Отдел="Номер отдела"
	AND Должность="Номер должности";
CREATE OR REPLACE VIEW Учёт."Данные о сменах" AS
	SELECT 	Смены."Табельный номер", "Дата смены", "Текущий оклад", "Начало смены",
	"Окончание смены", "Время работы", "Временные точки", Замечания, Зарплата
	FROM Учёт.Смены, Учёт.Работники
	WHERE Смены."Табельный номер" = Работники."Табельный номер";
CREATE OR REPLACE FUNCTION Учёт.auth_process(login varchar,  password varchar)
RETURNS text[]
LANGUAGE 'plpgsql'
AS
$$
DECLARE
	answer boolean;
	number varchar;
BEGIN
	answer = false;
	number = '';
	IF (SELECT COUNT (*) FROM Учёт.Аутентификации WHERE Логин = login AND Пароль = password) = 1 THEN
		answer = true;
		number = (SELECT Работник FROM Учёт.Аутентификации WHERE Логин = login AND Пароль = password);
	END IF;
	RETURN ARRAY[answer::text, number];
END;
$$;
ALTER TABLE Учёт.Работники ALTER COLUMN Позиция DROP NOT NULL;
ALTER TABLE Учёт.Аутентификации ALTER COLUMN Работник DROP NOT NULL;
ALTER TABLE Учёт.Смены ALTER COLUMN "Табельный номер" DROP NOT NULL;
ALTER TABLE Учёт.Смены ALTER COLUMN "Временные точки" DROP NOT NULL;
/*
SELECT * FROM information_schema.triggers WHERE trigger_schema='Учёт' AND trigger_name LIKE 'no_%';
*/