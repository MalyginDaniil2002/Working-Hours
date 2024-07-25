import PySimpleGUI as Gui
import psycopg2
STYLE = "Times New Roman"
ELEMENT_SIZE = 20
INPUT_SIZE = 20
DATES_SIZE = 5
TITLE = "Рабочий стол"
SCHEMA_NAME = 'Учёт'
VIEWS_LIST = ["Данные о сменах", "Данные о текущих работниках"]
NUMBER_NAME = '"Табельный номер"'
AUTH_FUNC = "SELECT {}.{}({})"
GET_VIEW = 'SELECT * FROM {}."{}" WHERE {} = {}'
DEFAULT = 'None'


def db_get(operation):
    try:
        with psycopg2.connect(dbname='times', user='postgres', password='14032002md',
                              host='localhost', port='5433') as connection:
            with connection.cursor() as cursor:
                cursor.execute(operation)
                get_column_names = [desc[0] for desc in cursor.description]
                get_values = cursor.fetchall()
        return get_values, get_column_names
    except psycopg2.Error:
        return 'no response', ''


def no_response():
    exit_button_text = 'ОК'
    window_title = "{} (Ошибка соединения)".format(TITLE)
    info_text_name = "Соединение с сервером не было установлено.\nПопробуйте ещё раз."
    auth_process_layout = [[Gui.Text(text=info_text_name, justification='center')],
                           [Gui.Button(button_text=exit_button_text)]]
    auth_process_window = Gui.Window(title=window_title, layout=auth_process_layout,
                                     element_justification='center', modal=True).Finalize()
    while True:
        event, values = auth_process_window.read()
        if event == Gui.WIN_CLOSED or event == exit_button_text:
            break
    auth_process_window.close()


def view_work(view_name, worker_number):
    back_to_menu_button_text = 'Назад в меню'
    window_title = "{} ({})".format(TITLE, view_name)
    column_names = []
    column_data = []
    data = []
    get_data, column_names = db_get(GET_VIEW.format(SCHEMA_NAME, view_name, NUMBER_NAME, "'{}'".format(worker_number)))
    for element in get_data:
        column_data.append(list(element))
    data_table = Gui.Table(values=column_data, headings=column_names, auto_size_columns=True, max_col_width=240,
                           justification='center', vertical_scroll_only=False, expand_y=True)
    back_button = Gui.Button(button_text=back_to_menu_button_text, expand_x=True)
    tables_window = Gui.Window(title=window_title, layout=[[data_table], [back_button]],
                               element_justification='center', modal=True).Finalize()
    tables_window.Maximize()
    while True:
        event, values = tables_window.read()
        if event == Gui.WIN_CLOSED or event == back_to_menu_button_text:
            break
    tables_window.close()


def auth_error():
    exit_button_text = 'ОК'
    window_title = "{} (Ошибка аутентификации))".format(TITLE)
    info_text_name = "Логин или пароль были введены неверно.\nПопробуйте ещё раз."
    auth_process_layout = [[Gui.Text(text=info_text_name, justification='center')],
                           [Gui.Button(button_text=exit_button_text)]]
    auth_process_window = Gui.Window(title=window_title, layout=auth_process_layout,
                                     element_justification='center', modal=True).Finalize()
    while True:
        event, values = auth_process_window.read()
        if event == Gui.WIN_CLOSED or event == exit_button_text:
            break
    auth_process_window.close()


def auth_process():
    response = DEFAULT
    exit_button_text = 'Выйти'
    window_title = "{} (аутентификация)".format(TITLE)
    auth_process_layout = [[Gui.Text(text="Здравствуйте! Введите ваш логин и пароль.", justification='center')],
                           [Gui.Text(text='Логин', size=(10, 1)), Gui.InputText()],
                           [Gui.Text(text='Пароль', size=(10, 1)), Gui.InputText()],
                           [Gui.Button(button_text='Авторизация', size=(26, 1)),
                            Gui.Button(button_text=exit_button_text, size=(26, 1))]]
    auth_process_window = Gui.Window(title="{} (аутентификация)".format(TITLE), element_padding=(10, 15),
                                     layout=auth_process_layout, element_justification='center', modal=True).Finalize()
    auth_process_window.Maximize()
    while True:
        event, values = auth_process_window.read()
        if event == Gui.WIN_CLOSED or event == exit_button_text:
            break
        else:
            params = "'{}', '{}'".format(values[0], values[1])
            checking, columns = db_get(AUTH_FUNC.format(SCHEMA_NAME, "auth_process", params))
            if checking != 'no response':
                if checking[0][0][0] == 'true':
                    response = checking[0][0][1]
                    break
                else:
                    auth_error()
            else:
                no_response()
    auth_process_window.close()
    return response


def view_select():
    exit_button_text = 'Выйти'
    window_title = "{} (Выбор отображения)".format(TITLE)
    info_text_name = "Выберите необходимую для отображения данные.\n" \
                     "Для этого нажмите на нужную кнопку."
    view_select_layout = [[Gui.Text(text=info_text_name, justification='center')]]
    for index in range(len(VIEWS_LIST)):
        view_select_layout.append([Gui.Button(button_text=VIEWS_LIST[index], key=index, expand_x=True, expand_y=True)])
    view_select_layout.append([Gui.Button(button_text=exit_button_text, expand_x=True, expand_y=True)])
    table_select_window = Gui.Window(title=window_title, layout=view_select_layout,
                                     element_justification='center', modal=True).Finalize()
    table_select_window.Maximize()
    response = auth_process()
    if response != DEFAULT:
        while True:
            event, values = table_select_window.read()
            if event == Gui.WIN_CLOSED or event == exit_button_text:
                break
            else:
                view_work(VIEWS_LIST[event], response)
    table_select_window.close()


if __name__ == "__main__":
    Gui.set_options(font=(STYLE, ELEMENT_SIZE))
    Gui.theme('DarkBrown2')
    view_select()
