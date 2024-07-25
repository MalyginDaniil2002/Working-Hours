------
select * from Учёт."Данные о сменах"
insert into Учёт.Должности(Название, "Начальный оклад") values ('Блогер', 120);
insert into Учёт.Должности(Название, "Начальный оклад") values ('Грузчик', 25);
insert into Учёт.Отделы(Название) values ('Отдел видеоблога');
insert into Учёт.Отделы(Название) values ('Отдел склада');
insert into Учёт."Должность-Отдел"(Отдел, Должность) values (2, 2);
insert into Учёт.Работники("Табельный номер", Фамилия, Имя, Отчество, "Дата рождения", Телефон, Почта, Позиция,
						   "Тип занятости") values ('321313', 'a', 'b', 'c', '2021-11-11', '2213', 'sdaa', 1, 'Фриланс');
insert into Учёт.Смены("Табельный номер", "Дата смены", "Начало смены", "Окончание смены") values
	('321313', '2024-12-12', '08:00:00', '21:00:00');
update Учёт.Работники set Позиция = 6 where Позиция isnull;
update Учёт.Смены set "Временные точки" = jsonb_set("Временные точки", '{"08:00:00"}', 'true') where "Номер смены" = 11;
--SELECT jsonb_set('{"1": true}'::jsonb, '{"1"}', 'false');
------
select * from Учёт.Должности;
select * from Учёт.Отделы;
select * from Учёт."Должность-Отдел";
select * from Учёт.Работники;
select * from Учёт.Аутентификации;
select * from Учёт.Смены;
update Учёт."Должность-Отдел" set Должность = 4 where Должность = 3;
update Учёт."Должность-Отдел" set Отдел = 4 where Отдел = 3;
update Учёт.Работники set "Табельный номер" = '3123' where "Табельный номер" = '321313';
update Учёт.Аутентификации set Логин='31312312r';
update Учёт.Смены set "Начало смены"='13:00:00';
update Учёт.Смены set Зарплата=3000;
update Учёт.Смены set Замечания=array_append(Замечания, 'Он - хуй');
delete from Учёт.Должности;
delete from Учёт.Отделы;
delete from Учёт."Должность-Отдел";
delete from Учёт.Работники;
delete from Учёт.Аутентификации;
delete from Учёт.Смены;

update Учёт.Смены
set "Временные точки" = jsonb_set("Временные точки", '{00:00:00}', 'true')
where "Номер смены" = 1;

update Учёт.Смены
set Замечания = '{}'
where "Номер смены" = 1;

update Учёт.Смены
set Замечания=array_append(Замечания, 'Он - хитёр\n')
where "Номер смены" = 2;

SELECT ('Привет' || E'\n' || 'мир');
SELECT Замечания FROM Учёт.Смены where "Номер смены" IN (1);
SELECT "Временные точки" FROM Учёт.Смены;
SELECT * FROM Учёт.Смены WHERE "Временные точки" ->> '24:00:00' = 'False';
SELECT * FROM Учёт.Смены WHERE Замечания[1] LIKE ('%Он%');
select * from information_schema.tables where table_schema = 'Учёт' AND table_type != 'VIEW' ;
select * from information_schema.columns where table_schema = 'Учёт';

SELECT tables.table_name, data_type
FROM information_schema.tables, information_schema.columns
WHERE tables.table_schema = 'Учёт' AND tables.table_name = columns.table_name AND tables.table_type != 'VIEW';

SELECT unnest(enum_range(NULL::Учёт."Типы занятости"))
SELECT data_type
FROM
(
	SELECT data_type, COUNT(data_type)
	FROM information_schema.tables, information_schema.columns
	WHERE tables.table_schema = 'Учёт' AND tables.table_name = columns.table_name AND tables.table_type != 'VIEW'
	GROUP BY data_type
) as tab;