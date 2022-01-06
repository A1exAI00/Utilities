'''
Конверер валют c GUI

DATE: 06.01.2022
AUTHOR: Alex Akinin
'''


import PySimpleGUI as sg
from forex_python.converter import CurrencyRates

currencies = ['RUB', 'USD', 'EUR', 'JPY', 'CHF']
input_key = ['-IRUB-', '-IDOL-', '-IEUR-', '-IJPY-', '-ICHF-']
output_key = ['-ORUB-', '-ODOL-', '-OEUR-', '-OJPY-', '-OCHF-']

curr_layout = [[sg.T('Рубли')],
               [sg.T('Доллары')], 
               [sg.T('Евро')],
               [sg.T('Йена')],
               [sg.T('Франки')],]

input_layout = [[sg.I('', key=tmp_key, size=(20,1))] for tmp_key in input_key]
output_layout =[[sg.T('', key=tmp_key, size=(10,1))] for tmp_key in output_key]

layout = [[sg.T('Скрипт переводит валюты.\nЗаполните только одно поле и нажмите "Перевести"\n"Очистить" для очистки полей ввода')],
          [sg.HSep()],
          [sg.Col(curr_layout), sg.VSep(), sg.Col(input_layout), sg.VSep(), sg.Col(output_layout)],
          [sg.B('Перевести'), sg.B('Очистить'), sg.B('Выход')]]
window = sg.Window('Перевод валют', layout)

sg.PopupNoButtons('Загрузка данных о курсах перевода.\nПожалуйста, подождите.', non_blocking=True, auto_close=True, auto_close_duration=7, no_titlebar=True)

# Создать лист для перевода 
try:
    c = CurrencyRates()
    # exchange_course = list([i+1 for i in range(len(input_key))])
    exchange_course = list([1/c.get_rate('RUB', currency) for currency in currencies])
except:
    sg.PopupError('Загрузка данных о курсах не удалась.', non_blocking=False, auto_close=True, auto_close_duration=7)
    exit()

while True: 
    event, values = window.read()
    if event in (None, 'Выход'):
        break

    if event == 'Очистить':
        for tmp_key in input_key:
            window[tmp_key].update('')
    
    if event != 'Перевести':
        continue

    curr_val = tuple((values[tmp_key] for tmp_key in input_key))

    if not any(curr_val):
        continue

    for i, tmp_key in enumerate(input_key):
        if values[tmp_key]:
            main_input_key = tmp_key
            main_input_key_num = i
            break
    
    if i == 0:
        rub_val = int(curr_val[main_input_key_num])
        window['-ORUB-'].update(rub_val)
    else:
        rub_val = int(curr_val[main_input_key_num]) * exchange_course[main_input_key_num]
        window['-ORUB-'].update(rub_val)
    
    for i, tmp_key in enumerate(output_key):
        window[tmp_key].update(round(rub_val / exchange_course[i], 1))
    




window.close()