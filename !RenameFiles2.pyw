'''
Скрипт с GUI для переименования файлов на основе метаданных

Пользователь выбирает папку с файлами
Скрипт по метаданным сортирует файлы
Создает новую папку sorted
И пытается скопировать туда сортированые файлы

version 0.2

DATE: 06.01.2022
AUTHOR: Alex Akinin
'''

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import os
import PySimpleGUI as sg
from pathlib import Path
from shutil import copy
from numpy.random import rand


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Создание лэйаута окна и самого окна
layout = [[sg.T('Cкрипт копирует все файлы в выбранной папке в новую папку sorted под новым именем.\nФормат нового имени: 0003.png', size=(50,3))],
        [sg.HSeparator()],
        [sg.T('Выберите папку с файлами:')],
        [sg.I('', key='-DIR-',), sg.FolderBrowse('Выбрать папку', target='-DIR-')],
        [sg.T('Сортировка по:'), sg.Combo(values=('Дата создания', 'Старое имя', 'Размер'), default_value='Дата создания', key='-COMBO-'), sg.Checkbox('Обратная сортировка', key='-REVERSE-')],
        [sg.T('Длина нового имени файлов:'), sg.I('4', key='-NAME LEN-', size=(20, 1))],
        [sg.T('Начать индексацию с числа:'), sg.I('0', key='-START INDEX-', size=(20, 1))],
        [sg.B('Ок', bind_return_key=True), sg.B('Отмена')],
        [sg.HSeparator()],
        [sg.T('Прогресс'), sg.ProgressBar(1000, orientation='h', size=(30, 20), key='-PROGRESS BAR-', bar_color=('green', 'white'))]]
window = sg.Window('Переименовать', layout)


folder_dir = ''
while True:
    event, values = window.read()
    window['-PROGRESS BAR-'].UpdateBar(0)
    

    # Проверка выхода из окна
    if event in (None,'Отмена'):
        break
    
    # Проверка нажатия на кнопку выбора папки

    folder_dir = values['-DIR-']
    if not folder_dir:
        continue
    if not Path(folder_dir).is_dir():
        sg.PopupError('Такой папки не существует', auto_close=True, auto_close_duration=3, non_blocking=True)
        continue

    # Проверка нажатия на кнопку Ок
    if event != 'Ок':
        continue
    
    # Проверка начального индекса
    try:
        start_index = int(values['-START INDEX-'])
    except:
        sg.PopupError('Индекс должен быть числом', auto_close=True, auto_close_duration=3, non_blocking=True)
        continue

    # Проверка длины имени
    try:
        name_len = int(values['-NAME LEN-'])
    except:
        sg.PopupError('Длина имени должна быть числом', auto_close=True, auto_close_duration=3, non_blocking=True)
        continue
    


    # Создать окно для подтверждения
    layout_oneshot = [[sg.T('Уверены в том, что хотите создать новую папку?')], [sg.B('Ок'), sg.B('Отмена')]]
    event_oneshot, values_oneshot = sg.Window("Title", layout_oneshot).read(close=True)
    if event_oneshot in (None, 'Отмена'):
        continue
        
    # Сбор файлов в папке
    file_names = os.listdir(folder_dir)
    files_path = ['/'.join([folder_dir,file]) for file in file_names]

    # Вытягивание данных о дате создания
    c_time, f_size = [], []
    for file_path in files_path:
        if Path(file_path).is_dir():
            continue
        stats = os.stat(file_path)
        print(stats)
        c_time.append(stats.st_ctime)
        f_size.append(stats.st_size)
    
    # Собрать данные о файлах в одну переменную
    data = list(zip(files_path, c_time, file_names, f_size))

    # Сортировка на основе выбранного параметра
    reverse_sort = values['-REVERSE-']
    if values['-COMBO-'] == 'Дата создания':
        data_sorted = sorted(data, key=lambda tup: tup[1], reverse=reverse_sort)
    elif values['-COMBO-'] == 'Старое имя':
        data_sorted = sorted(data, key=lambda tup: tup[2], reverse=reverse_sort)
    elif values['-COMBO-'] == 'Размер':
        data_sorted = sorted(data, key=lambda tup: tup[3], reverse=reverse_sort)

    for i in data_sorted:
        print(i)
    num_files = len(data_sorted)

    # Проверка, достаточно ли длины имени чтоб вместить количество файлов
    if len(str(num_files)) > name_len:
        sg.PopupError('Длина имени слишком маленькая по сравнению с количеством файлов', auto_close=True, auto_close_duration=3, non_blocking=True)
        continue

    
    # Создание новой папки с сортированными файлами
    newpath = '/'.join([folder_dir, 'sorted'])
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Копирование в папку sorted
    successful = True
    for i, file_tuple in enumerate(data_sorted):
        try:
            old_path = file_tuple[0]
            extention = old_path[old_path.index('.')+1:]
            zeros = '0' * (name_len-len(str(i)))
            copy(file_tuple[0], '/'.join([newpath, f'{zeros+str(i+start_index)}.{extention}']))
            window.refresh()
            window['-PROGRESS BAR-'].UpdateBar((i+1)/num_files * 1000)
        except:
            sg.PopupError('Что-то пошло не так.', auto_close=True, auto_close_duration=1, non_blocking=True, location=(int(700*rand()), int(700*rand())))
            successful = False
    
    # Окно удачного выполенния копирования
    if successful:
        sg.Popup('Удачно переименовано.', background_color='green')
    else:
        sg.Popup('Что-то переименовать не удалось.')



window.close()