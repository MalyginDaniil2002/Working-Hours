import PySimpleGUI as Gui
import psycopg2
DBNAME = 'times'
USER = 'postgres'
PASSWORD = '14032002md'
HOST = 'localhost'
PORT = '5433'
STYLE = "Times New Roman"
ELEMENT_SIZE = 20
INPUT_SIZE = 20
DATES_SIZE = 5
TITLE = "Управление учётом рабочего времени"
SCHEMA_NAME = 'Учёт'
DEFAULT_VALUES = ('', '----')
NULL_VALUE = None
ERROR_TEXT = "Ввод неверно выполнен в следующих полях рамки '{}':\n{}"
NO_INPUT_TEXT = "Вами не был выполнен ввод в рамку '{}'!"
BOOLEAN_DEFAULTS = (DEFAULT_VALUES[1], False, True)
DATES = ('День:', 'Месяц:', 'Год:')
SHOW_TABLE_EXECUTE = 'SELECT * FROM {}.'.format(SCHEMA_NAME)
INSERT_TABLE_EXECUTE = "INSERT INTO {}.{} ({}) VALUES {}"
UPDATE_TABLE_EXECUTE = "UPDATE {}.{} SET {}{}"
DELETE_TABLE_EXECUTE = "DELETE FROM {}.".format(SCHEMA_NAME)
ACTION_LIST = ('Добавить', 'Изменить', 'Изменить Точки/Замечания', 'Удалить')
DELETE_LIST = ('Удалить определённую строку', 'Удалить всё')
VIEW_LIST = ('Фильтр', 'Отмена фильтра')
FRAME_NAMES = ('{} Где', '{} Значения')
ENUM_NAME = "Типы занятости"
SPECIAL_TABLE = '"Смены"'
MONTH_LIST = []
for index in range(12):
    MONTH_LIST.append(index+1)
DAY_DICT = {1: 31, 2: [28, 29], 3: 31, 4: 30, 5: 31, 6: 30, 7: 30, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
TYPES = ('date', 'boolean', 'integer', 'character varying', 'numeric', 'interval', 'jsonb', 'ARRAY', 'USER-DEFINED')
with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
    with connection.cursor() as cursor:
        TABLES_LIST = []
        DATE_COLUMNS = []
        NO_INSERT_TABLE = '"Аутентификации"'
        BOOLEAN_COLUMNS = []
        ARRAY_COLUMNS = []
        INTEGER_COLUMNS = []
        VARCHAR_COLUMNS = []
        NUMERIC_COLUMNS = []
        TEXT_COLUMNS = []
        INTERVAL_COLUMNS = []
        JSONB_COLUMNS = []
        DEFINED_COLUMNS = []
        PRIMARY_KEY_COLUMNS = []
        FOREIGN_KEY_COLUMNS = []
        NO_INSERT_COLUMNS = ['"Смены"."Зарплата"', '"Смены"."Время работы"']
        VARCHAR_LENGTH = {}
        FOREIGN_KEY_TABLE = {}
        FOREIGN_KEY_TABLE_COLUMN = {}
        cursor.execute("SELECT tablename\n"
                       "FROM pg_catalog.pg_tables\n"
                       "WHERE schemaname=%s", (SCHEMA_NAME,))
        tables = cursor.fetchall()
        for elem in tables:
            TABLES_LIST.append('"{}"'.format(elem[0]))
        cursor.execute("SELECT table_name, column_name\n"
                       "FROM INFORMATION_SCHEMA.key_column_usage\n"
                       "WHERE table_schema=%s AND constraint_name IN (\n"
                       "    SELECT constraint_name\n"
                       "    FROM INFORMATION_SCHEMA.table_constraints\n"
                       "    WHERE constraint_type=%s)", (SCHEMA_NAME, 'PRIMARY KEY'))
        primary_keys = cursor.fetchall()
        for index in range(len(primary_keys)):
            primary_key = '"{}"."{}"'.format(primary_keys[index][0], primary_keys[index][1])
            PRIMARY_KEY_COLUMNS.append(primary_key)
        cursor.execute("WITH con_1 AS (\n"
                       "    SELECT constraint_name, table_name, column_name\n"
                       "    FROM INFORMATION_SCHEMA.key_column_usage\n"
                       "    WHERE table_schema=%s AND constraint_name IN (\n"
                       "        SELECT constraint_name\n"
                       "        FROM INFORMATION_SCHEMA.table_constraints\n"
                       "        WHERE constraint_type=%s)), con_2 AS(\n"
                       "    SELECT constraint_name, table_name, column_name\n"
                       "    FROM INFORMATION_SCHEMA.constraint_column_usage\n"
                       "    WHERE constraint_schema=%s)\n"
                       "SELECT con_1.table_name, con_1.column_name, con_2.table_name, con_2.column_name\n"
                       "FROM con_1 INNER JOIN con_2 USING(constraint_name)", (SCHEMA_NAME, 'FOREIGN KEY', SCHEMA_NAME,))
        col_keys = cursor.fetchall()
        for index in range(len(col_keys)):
            foreign_key = '"{}"."{}"'.format(col_keys[index][0], col_keys[index][1])
            primary_key = '"{}"."{}"'.format(col_keys[index][2], col_keys[index][3])
            FOREIGN_KEY_COLUMNS.append(foreign_key)
            FOREIGN_KEY_TABLE[foreign_key] = '"{}"'.format(col_keys[index][2])
            FOREIGN_KEY_TABLE_COLUMN[foreign_key] = primary_key
        for one_type in TYPES:
            cursor.execute("SELECT table_name, column_name\n"
                           "FROM INFORMATION_SCHEMA.COLUMNS\n"
                           "WHERE table_schema=%s AND data_type=%s", (SCHEMA_NAME, one_type))
            data = cursor.fetchall()
            if one_type == TYPES[0]:
                for elem in data:
                    DATE_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[1]:
                for elem in data:
                    BOOLEAN_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[2]:
                for elem in data:
                    INTEGER_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[3]:
                for elem in data:
                    VARCHAR_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
                cursor.execute("SELECT table_name, column_name, character_maximum_length\n"
                               "FROM INFORMATION_SCHEMA.COLUMNS\n"
                               "WHERE table_schema = '{}' AND data_type = '{}' "
                               "AND character_maximum_length <> {}".format(SCHEMA_NAME, one_type, 0))
                varchar_length = cursor.fetchall()
                for index in range(len(varchar_length)):
                    name = '"{}"."{}"'.format(varchar_length[index][0], varchar_length[index][1])
                    value = int(varchar_length[index][2])
                    VARCHAR_LENGTH[name] = value
            elif one_type == TYPES[4]:
                for elem in data:
                    NUMERIC_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[5]:
                for elem in data:
                    INTERVAL_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[6]:
                for elem in data:
                    JSONB_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            elif one_type == TYPES[7]:
                for elem in data:
                    ARRAY_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))
            else:
                for elem in data:
                    DEFINED_COLUMNS.append('"{}"."{}"'.format(elem[0], elem[1]))


def db_get(operation):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
        with connection.cursor() as cursor:
            cursor.execute(operation)
            get_column_names = [desc[0] for desc in cursor.description]
            get_values = cursor.fetchall()
    return get_values


def db_edit(operation):
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
            with connection.cursor() as cursor:
                cursor.execute(operation)
    except psycopg2.errors.CheckViolation:
        check_error()
    except psycopg2.errors.UniqueViolation:
        unique_error()


def no_input_error(frame_name):
    text = NO_INPUT_TEXT.format(frame_name)
    no_error_title = 'Сообщение об отсутствии ввода'
    no_error_layout = []
    no_error_text = Gui.Text(text=text, justification='center', key=0)
    no_error_button = Gui.Button(button_text='ОК', key=1, expand_x=True)
    no_error_layout = [[no_error_text], [no_error_button]]
    no_error_window = Gui.Window(title=no_error_title, layout=no_error_layout, modal=True).Finalize()
    while True:
        event, values = no_error_window.read()
        if event == 1:
            break
    no_error_window.close()


def check_error():
    text = 'Вы неверно ввели данные времени!'
    check_error_title = 'Сообщение об ошибке при вводе временных данных'
    no_error_text = Gui.Text(text=text, justification='center', key=0)
    no_error_button = Gui.Button(button_text='ОК', key=1, expand_x=True)
    check_error_layout = [[no_error_text], [no_error_button]]
    check_error_window = Gui.Window(title=check_error_title, layout=check_error_layout, modal=True).Finalize()
    while True:
        event, values = check_error_window.read()
        if event == 1:
            break
    check_error_window.close()


def unique_error():
    text = "Вы нарушили уникальность путём ввода одинаковой комбинации!\n" \
           "Введите верную комбинацию или измените существующую."
    check_error_title = 'Сообщение об ошибке при вводе ссылаемых полей'
    no_error_text = Gui.Text(text=text, justification='center', key=0)
    no_error_button = Gui.Button(button_text='ОК', key=1, expand_x=True)
    check_error_layout = [[no_error_text], [no_error_button]]
    check_error_window = Gui.Window(title=check_error_title, layout=check_error_layout, modal=True).Finalize()
    while True:
        event, values = check_error_window.read()
        if event == 1:
            break
    check_error_window.close()


def input_error(frame_name_1, problems_1, frame_name_2, problems_2):
    text = ''
    edit_problems_1 = []
    edit_problems_2 = []
    for index in range(len(problems_1)):
        edit_problems_1.append(problems_1[index])
    for index in range(len(problems_2)):
        edit_problems_2.append(problems_2[index])
    frame_problems_1 = ', '.join(edit_problems_1)
    frame_problems_2 = ', '.join(edit_problems_2)
    input_error_title = 'Сообщение о неверном вводе'
    if (len(problems_1) != 0) and (len(problems_2) != 0):
        add_text = '{}\n{}'.format(ERROR_TEXT, ERROR_TEXT)
        text = add_text.format(frame_name_1, frame_problems_1, frame_name_2, frame_problems_2)
    elif len(problems_1) != 0:
        text = ERROR_TEXT.format(frame_name_1, frame_problems_1)
    elif len(problems_2) != 0:
        text = ERROR_TEXT.format(frame_name_2, frame_problems_2)
    input_error_text = Gui.Text(text=text, justification='center', key=0)
    input_error_button = Gui.Button(button_text='ОК', key=1, expand_x=True)
    input_error_layout = [[input_error_text], [input_error_button]]
    input_error_window = Gui.Window(title=input_error_title, layout=input_error_layout, modal=True).Finalize()
    while True:
        event, values = input_error_window.read()
        if event == 1:
            break
    input_error_window.close()


def values_frame(elements_count, table_name, column_names):
    date_count = 0
    insert_count = 0
    primary_key_count = 0
    frame_layout = []
    insert_column_names = []
    for index in range(len(column_names)):
        index_number = 2*date_count+elements_count+index-insert_count-primary_key_count
        full_name = '{}.{}'.format(table_name, column_names[index])
        if full_name in PRIMARY_KEY_COLUMNS:
            if full_name not in INTEGER_COLUMNS:
                new_text = Gui.Text(text=column_names[index], expand_x=True)
                new_input = Gui.Input(default_text=DEFAULT_VALUES[0],
                                      key=index_number)
                frame_layout.append([new_text, new_input])
                insert_column_names.append(column_names[index])
            else:
                primary_key_count += 1
        elif full_name in FOREIGN_KEY_COLUMNS:
            keys = [(DEFAULT_VALUES[1])]
            get_values = 'SELECT {}\n'\
                         'FROM {}'.format(FOREIGN_KEY_TABLE_COLUMN[full_name],
                                          '{}.{}'.format(SCHEMA_NAME, FOREIGN_KEY_TABLE[full_name]))
            values = db_get(get_values)
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for elem in values:
                keys.append(elem)
            new_combo = Gui.Combo(keys, default_value=DEFAULT_VALUES[1], size=(INPUT_SIZE, 1), expand_x=True,
                                  readonly=False, key=index_number)
            frame_layout.append([new_text, new_combo])
            insert_column_names.append(column_names[index])
        elif full_name in DATE_COLUMNS:
            date_layout = []
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for times in range(len(DATES)):
                date_text = Gui.Text(text=DATES[times])
                date_layout.append(date_text)
                date_input = Gui.Input(default_text=DEFAULT_VALUES[0], size=(DATES_SIZE, 1), key=index_number+times)
                date_layout.append(date_input)
            date_count += 1
            date_frame = Gui.Frame("", [date_layout])
            frame_layout.append([new_text, date_frame])
            insert_column_names.append(column_names[index])
        elif full_name in NUMERIC_COLUMNS:
            if full_name not in NO_INSERT_COLUMNS:
                new_text = Gui.Text(text=column_names[index], expand_x=True)
                new_input = Gui.Input(default_text='', size=(INPUT_SIZE, 1), key=index_number)
                frame_layout.append([new_text, new_input])
                insert_column_names.append(column_names[index])
            else:
                insert_count += 1
        elif (full_name in VARCHAR_COLUMNS) or (full_name in INTEGER_COLUMNS):
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            new_input = Gui.Input(default_text=DEFAULT_VALUES[0], size=(INPUT_SIZE, 1), key=index_number)
            frame_layout.append([new_text, new_input])
            insert_column_names.append(column_names[index])
        elif (full_name in INTERVAL_COLUMNS) and (full_name not in NO_INSERT_COLUMNS):
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            new_input = Gui.Input(default_text='', size=(INPUT_SIZE, 1), key=index_number)
            frame_layout.append([new_text, new_input])
            insert_column_names.append(column_names[index])
        elif full_name in DEFINED_COLUMNS:
            keys = [(DEFAULT_VALUES[1])]
            values = db_get('SELECT unnest(enum_range(NULL::{}."{}"))'.format(SCHEMA_NAME, ENUM_NAME))
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for elem in values:
                keys.append(elem[0].translate({ord(i): None for i in '{}'}))
            new_combo = Gui.Combo(keys, default_value=DEFAULT_VALUES[1], size=(INPUT_SIZE, 1), expand_x=True,
                                  readonly=False, key=index_number)
            frame_layout.append([new_text, new_combo])
            insert_column_names.append(column_names[index])
    return frame_layout, insert_column_names, 2*date_count+elements_count+(
            len(column_names)-primary_key_count-insert_count)


def containers_frame(elements_count, table_name, column_names):
    containers_count = 0
    frame_layout = []
    update_containers_names = []
    for index in range(len(column_names)):
        index_number = elements_count+containers_count
        full_name = '{}.{}'.format(table_name, column_names[index])
        if (full_name in ARRAY_COLUMNS) or (full_name in JSONB_COLUMNS):
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            new_input = Gui.Input(default_text=DEFAULT_VALUES[0], size=(INPUT_SIZE, 1), key=index_number)
            frame_layout.append([new_text, new_input])
            update_containers_names.append(column_names[index])
            containers_count += 1
    return frame_layout, update_containers_names


def where_frame(table_name, column_names):
    date_count = 0
    frame_layout = []
    for index in range(len(column_names)):
        index_number = 2*date_count+index
        full_name = '{}.{}'.format(table_name, column_names[index])
        if (full_name in FOREIGN_KEY_COLUMNS) or ((full_name in PRIMARY_KEY_COLUMNS) and (full_name in VARCHAR_COLUMNS)):
            keys = [(DEFAULT_VALUES[1]), NULL_VALUE]
            if full_name in FOREIGN_KEY_COLUMNS:
                get_values = 'SELECT {}\n' \
                             'FROM {}'.format(FOREIGN_KEY_TABLE_COLUMN[full_name],
                                              '{}.{}'.format(SCHEMA_NAME, FOREIGN_KEY_TABLE[full_name]))
            else:
                get_values = 'SELECT {}\n' \
                             'FROM {}'.format(column_names[index], '{}.{}'.format(SCHEMA_NAME, table_name))
            values = db_get(get_values)
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for elem in values:
                keys.append(elem)
            new_combo = Gui.Combo(keys, default_value=DEFAULT_VALUES[1], size=(INPUT_SIZE, 1), expand_x=True,
                                  readonly=False, key=index_number)
            frame_layout.append([new_text, new_combo])
        elif full_name in DATE_COLUMNS:
            date_layout = []
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for times in range(len(DATES)):
                date_text = Gui.Text(text=DATES[times])
                date_layout.append(date_text)
                date_input = Gui.Input(default_text=DEFAULT_VALUES[0], size=(DATES_SIZE, 1), key=index_number+times)
                date_layout.append(date_input)
            date_count += 1
            date_frame = Gui.Frame("", [date_layout])
            frame_layout.append([new_text, date_frame])
        elif full_name in BOOLEAN_COLUMNS:
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            new_combo = Gui.Combo(BOOLEAN_DEFAULTS, size=(INPUT_SIZE, 1), default_value=BOOLEAN_DEFAULTS[0],
                                  expand_x=True, readonly=False, key=index_number)
            frame_layout.append([new_text, new_combo])
        elif full_name in DEFINED_COLUMNS:
            keys = [(DEFAULT_VALUES[1])]
            values = db_get('SELECT unnest(enum_range(NULL::{}."{}"))'.format(SCHEMA_NAME, ENUM_NAME))
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            for elem in values:
                keys.append(elem[0].translate({ord(i): None for i in '{}'}))
            new_combo = Gui.Combo(keys, default_value=DEFAULT_VALUES[1], size=(INPUT_SIZE, 1), expand_x=True,
                                  readonly=False, key=index_number)
            frame_layout.append([new_text, new_combo])
        else:
            new_text = Gui.Text(text=column_names[index], expand_x=True)
            new_input = Gui.Input(default_text=DEFAULT_VALUES[0], size=(INPUT_SIZE, 1), key=index_number)
            frame_layout.append([new_text, new_input])
    return frame_layout, 2*date_count+len(column_names)


def values_frame_input_check(elements_count, table_name, values, column_names):
    date_count = 0
    insert_count = 0
    primary_key_count = 0
    check_date = True
    dates = []
    problems = []
    numbers_check = []
    integer_check = []
    numeric_check = []
    insert_values = []
    for i in range(10):
        numbers_check.append(str(i))
        integer_check.append(str(i))
        numeric_check.append(str(i))
    integer_check.append(' ')
    numeric_check.append('.')
    for index in range(len(column_names)):
        index_number = 2*date_count+elements_count+index-insert_count-primary_key_count
        full_name = table_name + '.' + column_names[index]
        if full_name in PRIMARY_KEY_COLUMNS:
            if full_name not in INTEGER_COLUMNS:
                repeat_count = db_get("SELECT COUNT({})\n"
                                      "FROM {}\n"
                                      "WHERE {}='{}'".format(column_names[index],
                                                             '{}.{}'.format(SCHEMA_NAME, table_name),
                                                             column_names[index], values[index_number]))[0][0]
                if int(repeat_count) != 0:
                    problems.append(column_names[index])
            else:
                primary_key_count += 1
        elif full_name in FOREIGN_KEY_COLUMNS:
            foreign_keys = db_get('SELECT {}\n'
                                  'FROM {}'.format(FOREIGN_KEY_TABLE_COLUMN[full_name],
                                                   '{}.{}'.format(SCHEMA_NAME, FOREIGN_KEY_TABLE[full_name])))
            if (values[index_number] not in foreign_keys) and (values[index_number] not in DEFAULT_VALUES):
                problems.append(column_names[index])
        elif full_name in BOOLEAN_COLUMNS:
            if values[index_number] not in BOOLEAN_DEFAULTS:
                problems.append(column_names[index])
        elif full_name in VARCHAR_LENGTH:
            if len(values[index_number]) > VARCHAR_LENGTH[full_name]:
                problems.append(column_names[index])
        elif full_name in NUMERIC_COLUMNS:
            if full_name not in NO_INSERT_COLUMNS:
                error_count = sum(values[index_number][element] not in numeric_check
                                  for element in range(len(values[index_number])))
                if error_count != 0:
                    problems.append(column_names[index])
                else:
                    if values[index_number].count('.') > 1:
                        problems.append(column_names[index])
            else:
                insert_count += 1
        elif full_name in INTEGER_COLUMNS:
            error_count = sum(values[index_number][element] not in integer_check
                              for element in range(len(values[index_number])))
            if error_count != 0:
                problems.append(column_names[index])
        elif full_name in DATE_COLUMNS:
            check_date_count = sum(values[index_number+times] == DEFAULT_VALUES[0]
                                   for times in range(len(DATES)))
            if (check_date_count > 0) and (check_date_count < 3):
                problems.append(column_names[index])
            elif check_date_count == 0:
                date = []
                for times in range(len(DATES)):
                    error_count = sum(values[index_number+times][element] not in numbers_check
                                      for element in range(len(values[index_number+times])))
                    if error_count != 0:
                        problems.append(column_names[index])
                        check_date = False
                        break
                    else:
                        date.append(int(values[index_number+times]))
                if check_date:
                    if date[1] not in MONTH_LIST:
                        problems.append(column_names[index])
                    else:
                        if type(DAY_DICT[date[1]]) is list:
                            if date[2] % 4 == 0:
                                max_day = DAY_DICT[date[1]][1]
                            else:
                                max_day = DAY_DICT[date[1]][0]
                            if (date[0] > max_day) and (date[0] == 0):
                                problems.append(column_names[index])
                        else:
                            if (date[0] > DAY_DICT[date[1]]) or (date[0] == 0):
                                problems.append(column_names[index])
                if column_names[index] not in problems:
                    dates.append([date][0])
            date_count += 1
        elif (full_name in ARRAY_COLUMNS) and (values[index_number] not in DEFAULT_VALUES):
            array = values[index_number].split(';')
            if (len(array) != 2) or (not array[0].isdigit()):
                problems.append(column_names[index])
        elif (full_name in JSONB_COLUMNS) and (values[index_number] not in DEFAULT_VALUES):
            jsonb = values[index_number].split(';')
            if len(jsonb) != 2:
                problems.append(column_names[index])
            else:
                jsonb_interval = jsonb[0].split(':')
                if len(jsonb_interval) != 3:
                    problems.append(column_names[index])
                elif (jsonb[1] != 'true') and (jsonb[1] != 'false'):
                    problems.append(column_names[index])
                for interval_index in range(len(jsonb_interval)):
                    if not jsonb_interval[interval_index].isdigit():
                        problems.append(column_names[index])
                        break
                    middle_value = int(jsonb_interval[interval_index])
                    if (interval_index == 0) and not (middle_value < 24):
                        problems.append(column_names[index])
                    if (interval_index != 0) and not (middle_value == 0):
                        problems.append(column_names[index])
        elif (full_name in INTERVAL_COLUMNS) and (full_name not in NO_INSERT_COLUMNS):
            interval_array = values[index_number].split(':')
            if len(interval_array) == 3:
                for interval_index in range(len(interval_array)):
                    if not interval_array[interval_index].isdigit():
                        problems.append(column_names[index])
                        break
                    middle_value = int(interval_array[interval_index])
                    if (interval_index == 0) and not (middle_value < 24):
                        problems.append(column_names[index])
                    if (interval_index != 0) and not (middle_value < 60):
                        problems.append(column_names[index])
            else:
                problems.append(column_names[index])
        if full_name in FOREIGN_KEY_COLUMNS:
            if full_name in INTEGER_COLUMNS:
                insert_values.append(values[index_number][0])
            elif full_name in VARCHAR_COLUMNS:
                insert_values.append('{}'.format(values[index_number][0]))
        elif (full_name in PRIMARY_KEY_COLUMNS) and (full_name in VARCHAR_COLUMNS):
            insert_values.append(values[index_number])
        elif (full_name in INTERVAL_COLUMNS) and (full_name not in NO_INSERT_COLUMNS):
            insert_values.append('{}'.format(values[index_number]))
        elif full_name in DATE_COLUMNS:
            if values[index_number] not in DEFAULT_VALUES:
                insert_values.append('{}.{}.{}'.format(values[index_number + DATES.index('День:')],
                                                       values[index_number + DATES.index('Месяц:')],
                                                       values[index_number + DATES.index('Год:')]))
            else:
                insert_values.append(values[index_number])
        elif (full_name in ARRAY_COLUMNS) and (values[index_number] not in DEFAULT_VALUES):
            if column_names[index] not in problems:
                middle_array = values[index_number].split(';')
                insert_values.append("{}[{}] = '{}) {}'".format(column_names[index], middle_array[0],
                                                                middle_array[0], middle_array[1]))
        elif full_name in JSONB_COLUMNS and (values[index_number] not in DEFAULT_VALUES):
            if column_names[index] not in problems:
                middle_jsonb = values[index_number].split(';')
                insert_values.append("{} = jsonb_set({}, '{}', '{}')".format(column_names[index], column_names[index],
                                                                             "{"+middle_jsonb[0]+"}", middle_jsonb[1]))
        elif (full_name not in PRIMARY_KEY_COLUMNS) and (full_name not in NO_INSERT_COLUMNS):
            insert_values.append(values[index_number])
    return problems, insert_values


def where_frame_input_check(table_name, values, column_names):
    date_count = 0
    check_date = True
    problems = []
    date_check = []
    integer_check = []
    numeric_check = []
    insert_values = []
    for i in range(10):
        date_check.append(str(i))
        integer_check.append(str(i))
        numeric_check.append(str(i))
    integer_check.append(' ')
    numeric_check.append(' ')
    numeric_check.append('.')
    for index in range(len(column_names)):
        index_number = 2*date_count+index
        full_name = table_name + '.' + column_names[index]
        if full_name in FOREIGN_KEY_COLUMNS:
            foreign_keys = db_get('SELECT {}\n'
                                  'FROM {}'.format(FOREIGN_KEY_TABLE_COLUMN[full_name],
                                                   '{}.{}'.format(SCHEMA_NAME, FOREIGN_KEY_TABLE[full_name])))
            if values[index_number] != NULL_VALUE:
                if (values[index_number] not in foreign_keys) and (values[index_number] not in DEFAULT_VALUES):
                    problems.append(column_names[index])
        elif full_name in BOOLEAN_COLUMNS:
            if values[index_number] not in BOOLEAN_DEFAULTS:
                problems.append(column_names[index])
        elif full_name in NUMERIC_COLUMNS:
            error_count = sum(values[index_number][element] not in numeric_check
                              for element in range(len(values[index_number])))
            if error_count != 0:
                problems.append(column_names[index])
            else:
                for elem in values[index_number].split():
                    if elem.count('.') > 1:
                        problems.append(column_names[index])
                        break
        elif full_name in INTEGER_COLUMNS:
            error_count = sum(values[index_number][element] not in integer_check
                              for element in range(len(values[index_number])))
            if error_count != 0:
                problems.append(column_names[index])
        elif full_name in DATE_COLUMNS:
            check_date_count = sum(values[index_number+times] == DEFAULT_VALUES[0]
                                   for times in range(len(DATES)))
            if (check_date_count > 0) and (check_date_count < 3):
                problems.append(column_names[index])
            elif check_date_count == 0:
                date = []
                for times in range(len(DATES)):
                    error_count = sum(values[index_number+times][element] not in date_check
                                      for element in range(len(values[index_number+times])))
                    if error_count != 0:
                        problems.append(column_names[index])
                        check_date = False
                        break
                    else:
                        date.append(int(values[index_number+times]))
                if check_date:
                    if date[1] not in MONTH_LIST:
                        problems.append(column_names[index])
                    else:
                        if type(DAY_DICT[date[1]]) is list:
                            if date[2] % 4 == 0:
                                max_day = DAY_DICT[date[1]][1]
                            else:
                                max_day = DAY_DICT[date[1]][0]
                            if (date[0] > max_day) and (date[0] == 0):
                                problems.append(column_names[index])
                        else:
                            if (date[0] > DAY_DICT[date[1]]) or (date[0] == 0):
                                problems.append(column_names[index])
            date_count += 1
        elif full_name in INTERVAL_COLUMNS:
            interval_array = values[index_number].split(':')
            if len(interval_array) == 3:
                for interval_index in range(len(interval_array)):
                    if not interval_array[interval_index].isdigit():
                        problems.append(column_names[index])
                        break
                    middle_value = int(interval_array[interval_index])
                    if (interval_index == 0) and not (middle_value < 24):
                        problems.append(column_names[index])
                    if (interval_index != 0) and not (middle_value < 60):
                        problems.append(column_names[index])
            elif values[index_number] not in DEFAULT_VALUES:
                problems.append(column_names[index])
        elif full_name in ARRAY_COLUMNS:
            array = values[index_number].split(';')
            if ((len(array) != 2) or (not array[0].isdigit())) and (values[index_number] not in DEFAULT_VALUES):
                problems.append(column_names[index])
        elif full_name in JSONB_COLUMNS:
            jsonb = values[index_number].split(';')
            if (len(jsonb) != 2) and (values[index_number] not in DEFAULT_VALUES):
                problems.append(column_names[index])
    return problems


def where_function(table_name, column_names, values, action_name):
    date_count = 0
    part_operation = ' WHERE '
    filters = []
    for index in range(len(column_names)):
        index_number = 2*date_count+index
        full_name = '{}.{}'.format(table_name, column_names[index])
        if values[2*date_count+index] not in DEFAULT_VALUES:
            if full_name in FOREIGN_KEY_COLUMNS:
                if values[index_number] == NULL_VALUE:
                    filters.append('{} is {}'.format(column_names[index], 'Null'))
                else:
                    if full_name in INTEGER_COLUMNS:
                        filters.append('{} = {}'.format(column_names[index], values[index_number][0]))
                    if full_name in VARCHAR_COLUMNS:
                        filters.append('{} = {}'.format(column_names[index], "'{}'".format(values[index_number][0])))
            elif full_name in DATE_COLUMNS:
                date = []
                date_count += 1
                for element in range(len(DATES)):
                    if element != 2:
                        if len(values[index_number+element]) == 1:
                            date.append('0{}'.format(values[index_number+element]))
                        else:
                            date.append(values[index_number+element])
                    else:
                        date.append(values[index_number+element])
                filters.append("{} = '{}'".format(column_names[index], '.'.join(date)))
            elif (full_name in INTEGER_COLUMNS) or (full_name in NUMERIC_COLUMNS):
                numbers = values[index_number].split()
                filters.append('{} IN ({})'.format(column_names[index], ', '.join(numbers)))
            elif full_name in DEFINED_COLUMNS:
                filters.append('{} = {}'.format(column_names[index], "'{}'".format(values[index_number])))
            elif full_name in VARCHAR_COLUMNS:
                if (action_name == VIEW_LIST[0]) and (full_name not in PRIMARY_KEY_COLUMNS):
                    filters.append("{} LIKE '%{}%'".format(column_names[index], values[index_number]))
                else:
                    if type(values[index_number]) == tuple:
                        filters.append("{} = '{}'".format(column_names[index], values[index_number][0]))
                    else:
                        filters.append("{} = '{}'".format(column_names[index], values[index_number]))
            elif full_name in INTERVAL_COLUMNS:
                filters.append("{} = '{}'".format(column_names[index], values[index_number]))
            elif full_name in ARRAY_COLUMNS:
                middle_array = values[index_number].split(';')
                filters.append("{}[{}] LIKE '%{}%'".format(column_names[index], middle_array[0], middle_array[1]))
            elif full_name in JSONB_COLUMNS:
                middle_jsonb = values[index_number].split(';')
                filters.append("{} ->> '{}' = '{}'".format(column_names[index], middle_jsonb[0], middle_jsonb[1]))
        elif full_name in DATE_COLUMNS:
            date_count += 1
    part_operation += ' AND '.join(filters)
    return part_operation


def insert_action(table_name, column_names, window_title, action_name):
    partial_count = 0
    new_values = ''
    frame_name = FRAME_NAMES[1].format(action_name)
    action_window_title = '{} ({} данных)'.format(window_title, ACTION_LIST[0])
    frame_layout, insert_column_names, total_count = values_frame(partial_count, table_name, column_names)
    insert_frame = [Gui.Frame(frame_name, frame_layout, expand_x=True)]
    insert_action_layout = [[Gui.Column([insert_frame], scrollable=True, expand_x=True)]]
    insert_button = Gui.Button(button_text=action_name, expand_x=True)
    back_button = Gui.Button(button_text='Назад к таблице', expand_x=True)
    insert_action_layout.append([insert_button, back_button])
    insert_action_window = Gui.Window(title=action_window_title, layout=insert_action_layout, modal=True)
    while True:
        event, values = insert_action_window.read()
        if event == Gui.WIN_CLOSED or event != action_name:
            break
        else:
            no_input_count = sum(values[index] in DEFAULT_VALUES for index in range(len(values)))
            if no_input_count == 0:
                problem_columns, insert_values = values_frame_input_check(partial_count, table_name,
                                                                          values, insert_column_names)
                if len(problem_columns) == 0:
                    if len(insert_values) > 1:
                        insert_operation = INSERT_TABLE_EXECUTE.format(SCHEMA_NAME, table_name,
                                                                       ','.join(insert_column_names),
                                                                       tuple(insert_values))
                    else:
                        if insert_values[0].isdigit():
                            middle_value = "'{}'".format(insert_values[0])
                        else:
                            middle_value = insert_values[0]
                        insert_operation = INSERT_TABLE_EXECUTE.format(SCHEMA_NAME, table_name,
                                                                       ','.join(insert_column_names),
                                                                       "('{}')".format(insert_values[0]))
                    db_edit(insert_operation)
                    break
                else:
                    input_error('', [], frame_name, problem_columns)
            else:
                no_input_error(frame_name)
    insert_action_window.close()
    return db_get(SHOW_TABLE_EXECUTE+table_name)


def update_action(table_name, column_names, window_title, action_name):
    new_values = ''
    frame_name_1 = FRAME_NAMES[0].format(action_name)
    frame_name_2 = FRAME_NAMES[1].format(action_name)
    action_window_title = '{} ({} данных)'.format(window_title, ACTION_LIST[1])
    frame_layout_1, partial_count = where_frame(table_name, column_names)
    update_frame_1 = [Gui.Frame(frame_name_1, frame_layout_1, expand_x=True)]
    frame_layout_2, update_column_names, total_count = values_frame(partial_count, table_name, column_names)
    update_frame_2 = [Gui.Frame(frame_name_2, frame_layout_2, expand_x=True)]
    update_action_layout = [[Gui.Column([update_frame_1], size=(100, 125), scrollable=True, expand_x=True)],
                            [Gui.Column([update_frame_2], size=(100, 125), scrollable=True, expand_x=True)]]
    update_button = Gui.Button(button_text=action_name, expand_x=True)
    back_button = Gui.Button(button_text='Назад к таблице', expand_x=True)
    update_action_layout.append([update_button, back_button])
    update_action_window = Gui.Window(title=action_window_title, layout=update_action_layout, modal=True)
    while True:
        event, values = update_action_window.read()
        if event == Gui.WIN_CLOSED or event != action_name:
            break
        else:
            no_input_count_2 = sum((values[index] not in DEFAULT_VALUES) and (index >= partial_count)
                                   for index in range(len(values)))
            no_input_count_1 = sum((values[index] not in DEFAULT_VALUES) and (index < partial_count)
                                   for index in range(len(values)))
            if no_input_count_2 != 0:
                problem_columns_1 = where_frame_input_check(table_name, values, column_names)
                problem_columns_2, update_values = values_frame_input_check(partial_count, table_name,
                                                                            values, column_names)
                if (len(problem_columns_1) == 0) and (len(problem_columns_2) == 0):
                    update_where = ''
                    update_sets = []
                    for value_index in range(len(update_column_names)):
                        if sum(str(update_values[value_index]) in elem for elem in DEFAULT_VALUES) == 0:
                            if isinstance(update_values[value_index], str):
                                update_sets.append("{}='{}'".format(update_column_names[value_index],
                                                                    update_values[value_index]))
                            else:
                                update_sets.append("{}='{}'".format(update_column_names[value_index],
                                                                    update_values[value_index]))
                    if no_input_count_1 != 0:
                        update_where = where_function(table_name, column_names, values, action_name)
                    update_operation = UPDATE_TABLE_EXECUTE.format(SCHEMA_NAME, table_name,
                                                                   ','.join(update_sets), update_where)
                    db_edit(update_operation)
                    break
                else:
                    input_error(frame_name_1, problem_columns_1, frame_name_2, problem_columns_2)
            else:
                no_input_error(frame_name_2)
    update_action_window.close()
    return db_get(SHOW_TABLE_EXECUTE+table_name)


def update_containers(table_name, column_names, window_title, action_name):
    new_values = ''
    frame_name_1 = FRAME_NAMES[0].format(action_name)
    frame_name_2 = FRAME_NAMES[1].format(action_name)
    action_window_title = '{} ({} данных)'.format(window_title, action_name)
    frame_layout_1, partial_count = where_frame(table_name, column_names)
    update_frame_1 = [Gui.Frame(frame_name_1, frame_layout_1, expand_x=True)]
    frame_layout_2, update_column_names = containers_frame(partial_count, table_name, column_names)
    update_frame_2 = [Gui.Frame(frame_name_2, frame_layout_2, expand_x=True)]
    update_containers_layout = [[Gui.Column([update_frame_1], size=(100, 125), scrollable=True, expand_x=True)],
                                [Gui.Column([update_frame_2], size=(100, 125), scrollable=True, expand_x=True)]]
    update_button = Gui.Button(button_text=action_name, expand_x=True)
    back_button = Gui.Button(button_text='Назад к таблице', expand_x=True)
    update_containers_layout.append([update_button, back_button])
    update_containers_window = Gui.Window(title=action_window_title, layout=update_containers_layout, modal=True)
    while True:
        event, values = update_containers_window.read()
        if event == Gui.WIN_CLOSED or event != action_name:
            break
        else:
            no_input_count_2 = sum((values[index] not in DEFAULT_VALUES) and (index >= partial_count)
                                   for index in range(len(values)))
            no_input_count_1 = sum((values[index] not in DEFAULT_VALUES) and (index < partial_count)
                                   for index in range(len(values)))
            if no_input_count_2 != 0:
                problem_columns_1 = where_frame_input_check(table_name, values, column_names)
                problem_columns_2, update_values = values_frame_input_check(partial_count, table_name,
                                                                            values, update_column_names)
                if (len(problem_columns_1) == 0) and (len(problem_columns_2) == 0):
                    update_where = ''
                    update_sets = []
                    for value_index in range(len(update_column_names)):
                        if sum(str(update_values[value_index]) in elem for elem in DEFAULT_VALUES) == 0:
                            update_sets.append(update_values[value_index])
                    if no_input_count_1 != 0:
                        update_where = where_function(table_name, column_names, values, action_name)
                    update_operation = UPDATE_TABLE_EXECUTE.format(SCHEMA_NAME, table_name,
                                                                   ','.join(update_sets), update_where)
                    db_edit(update_operation)
                    break
                else:
                    input_error(frame_name_1, problem_columns_1, frame_name_2, problem_columns_2)
            else:
                no_input_error(frame_name_2)
    update_containers_window.close()
    return db_get(SHOW_TABLE_EXECUTE+table_name)


def delete_action(table_name, column_names, window_title, action_name):
    new_values = ''
    frame_name = FRAME_NAMES[0].format(action_name)
    operation = DELETE_TABLE_EXECUTE + table_name
    action_window_title = '{} ({} данных)'.format(window_title, ACTION_LIST[3])
    buttons = []
    frame_layout, total_count = where_frame(table_name, column_names)
    delete_frame = [Gui.Frame(frame_name, frame_layout, expand_x=True)]
    delete_action_layout = [[Gui.Column([delete_frame], scrollable=True, expand_x=True)]]
    for index in range(len(DELETE_LIST)):
        delete_button = Gui.Button(button_text=DELETE_LIST[index], expand_x=True)
        buttons.append(delete_button)
    back_button = Gui.Button(button_text='Назад к таблице', key=total_count, expand_x=True)
    buttons.append(back_button)
    delete_action_layout.append([buttons])
    delete_action_window = Gui.Window(title=action_window_title, layout=delete_action_layout, modal=True)
    while True:
        event, values = delete_action_window.read()
        if event == Gui.WIN_CLOSED or event == total_count:
            break
        elif event == DELETE_LIST[-1]:
            db_edit(operation)
            break
        else:
            no_input_count = sum(values[index] in DEFAULT_VALUES for index in range(len(values)))
            if no_input_count < len(values):
                problem_columns = where_frame_input_check(table_name, values, column_names)
                if len(problem_columns) == 0:
                    delete_operation = operation + where_function(table_name, column_names, values, action_name)
                    db_edit(delete_operation)
                    break
                else:
                    input_error(frame_name, problem_columns, '', [])
            else:
                no_input_error(frame_name)
    delete_action_window.close()
    return db_get(SHOW_TABLE_EXECUTE+table_name)


def data_filter(table_name, column_names, window_title, action_name):
    new_values = ''
    frame_name = FRAME_NAMES[0].format(action_name)
    operation = SHOW_TABLE_EXECUTE + table_name
    view_window_title = '{} ({})'.format(window_title, action_name)
    frame_layout, elements_count = where_frame(table_name, column_names)
    filter_frame = [Gui.Frame(frame_name, frame_layout, expand_x=True)]
    filter_layout = [[Gui.Column([filter_frame], scrollable=True, expand_x=True)]]
    filter_button = Gui.Button(button_text='Отфильтровать', key=elements_count, expand_x=True)
    back_button = Gui.Button(button_text='Назад к таблице', key=elements_count+1, expand_x=True)
    filter_layout.append([filter_button, back_button])
    filter_window = Gui.Window(title=view_window_title, layout=filter_layout, modal=True)
    while True:
        event, values = filter_window.read()
        if event == Gui.WIN_CLOSED or event == elements_count+1:
            break
        else:
            no_count = sum(values[index] in DEFAULT_VALUES for index in range(len(values)))
            if no_count < len(values):
                problem_columns = where_frame_input_check(table_name, values, column_names)
                if len(problem_columns) == 0:
                    filter_operation = operation + where_function(table_name, column_names, values, action_name)
                    new_values = db_get(filter_operation)
                    break
                else:
                    input_error(frame_name, problem_columns, '', [])
            else:
                no_input_error(frame_name)
    filter_window.close()
    return new_values


def table_work(table_name):
    back_to_menu_button_text = 'Назад в меню'
    title_name = "'{}'".format(table_name)
    window_title = "{} - Таблица {}".format(TITLE, title_name)
    data = []
    main_table = []
    view_layout = []
    table_layout = []
    action_layout = []
    column_names_copy = []
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SHOW_TABLE_EXECUTE+table_name)
            column_names = [desc[0] for desc in cursor.description]
            get_data = cursor.fetchall()
    for index in range(len(column_names)):
        column_names[index] = '"{}"'.format(column_names[index])
    for elem in get_data:
        data.append(list(elem))
    if table_name == SPECIAL_TABLE:
        data_table = Gui.Table(values=data, headings=column_names, auto_size_columns=True,  max_col_width=240,
                               justification='center', vertical_scroll_only=False, key=0, expand_y=True)
    else:
        data_table = Gui.Table(values=data, headings=column_names, auto_size_columns=True,
                               justification='center', vertical_scroll_only=False, key=0, expand_x=True, expand_y=True)
    for index in range(len(ACTION_LIST)):
        if (table_name == SPECIAL_TABLE) or (index != 2):
            action_layout.append(Gui.Button(button_text=ACTION_LIST[index], expand_x=True))
    change_frame = Gui.Frame("Изменить данные", [action_layout], expand_x=True)
    for index in range(len(VIEW_LIST)):
        if index != 2:
            view_layout.append(Gui.Button(button_text=VIEW_LIST[index], expand_x=True))
    view_frame = Gui.Frame("Просмотр", [view_layout], expand_x=True)
    back_button = Gui.Button(button_text=back_to_menu_button_text, expand_x=True)
    if table_name != NO_INSERT_TABLE:
        table_layout = [[data_table], [change_frame], [view_frame], [back_button]]
    else:
        table_layout = [[data_table], [view_frame], [back_button]]
    tables_window = Gui.Window(title=window_title, layout=table_layout,
                               element_justification='center', modal=True).Finalize()
    tables_window.Maximize()
    while True:
        event, values = tables_window.read()
        if event == Gui.WIN_CLOSED or event == back_to_menu_button_text:
            break
        elif event in VIEW_LIST:
            if event == VIEW_LIST[0]:
                new_data = data_filter(table_name, column_names, window_title, event)
                if new_data != DEFAULT_VALUES[0]:
                    tables_window[0].update(new_data)
            else:
                tables_window[0].update(db_get(SHOW_TABLE_EXECUTE+table_name))
        else:
            if event == ACTION_LIST[0]:
                tables_window[0].update(insert_action(table_name, column_names, window_title, event))
            elif event == ACTION_LIST[1]:
                tables_window[0].update(update_action(table_name, column_names, window_title, event))
            elif event == ACTION_LIST[3]:
                tables_window[0].update(delete_action(table_name, column_names, window_title, event))
            else:
                tables_window[0].update(update_containers(table_name, column_names, window_title, event))
    tables_window.close()


def table_select():
    exit_button_text = 'Выход'
    window_title = "{} - Выбор таблицы".format(TITLE)
    info_text_name = "Выберите необходимую для работы таблицы нажатием на соотвествующую кнопку ниже.\n" \
                     "Для из приложения выхода можете нажать на самую последнюю кнопку."
    info_text = [Gui.Text(text=info_text_name, justification='center')]
    table_select_layout = [info_text]
    for index in range(len(TABLES_LIST)):
        new_button = Gui.Button(button_text=TABLES_LIST[index], key=index, expand_x=True, expand_y=True)
        table_select_layout.append([new_button])
    exit_button = [Gui.Button(button_text=exit_button_text, expand_x=True, expand_y=True)]
    table_select_layout.append(exit_button)
    table_select_window = Gui.Window(title=window_title, layout=table_select_layout,
                                     element_justification='center', modal=True).Finalize()
    table_select_window.Maximize()
    while True:
        event, values = table_select_window.read()
        if event == Gui.WIN_CLOSED or event == exit_button_text:
            break
        else:
            table_work(TABLES_LIST[event])
    table_select_window.close()


if __name__ == "__main__":
    Gui.set_options(font=(STYLE, ELEMENT_SIZE))
    Gui.theme('DarkBrown5')
    table_select()
