# -*- coding: utf-8 -*-
"""
Оконный генератор паролей

DATE: 08.01.2022
AUTHOR: Alex Akinin
"""

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

from random import choice as choice
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Checkbox
import re

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

def create_password(config, length):

    # Различные символы
    engL = 'abcdefghijklmnopqrstuvwxyz'
    engU = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    spec = '!#$%&()*+-=?@[]~_'
    numb = '0123456789'
    alphs = [numb, engL, engU, spec]

    # Сборка алфавита и пароля
    alph = ''.join([alphs[i] for i in range(4) if config[i]])
    return ''.join([choice(alph) for _ in range(int(length))])


def check_password(password, config):

    # Создание объектов регулярных выражений
    dig_reg = re.compile(r'(\d)')
    low_reg = re.compile(r'([a-z])')
    upp_reg = re.compile(r'([A-Z])')
    spe_reg = re.compile(r'([^abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789])')
    
    # Проверка пароля
    if config[0][0]:
        if len(dig_reg.findall(password)) < config[0][1]:
            return False
    if config[1][0]:
        if len(low_reg.findall(password)) < config[1][1]:
            return False
    if config[2][0]:
        if len(upp_reg.findall(password)) < config[2][1]:
            return False
    if config[3][0]:
        if len(spe_reg.findall(password)) < config[3][1]:
            return False
    
    return True


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

col1 = [[sg.Checkbox('Цифры', key='-NUMS-', default=True)],
        [sg.Checkbox('Маленькие буквы', key='-LOWS-', default=True)],
        [sg.Checkbox('Большие буквы', key='-UPPS-', default=True)],
        [sg.Checkbox('!#$%&()*+-=?@[~_', key='-SPEC-', default=True)]]

col2 = [[sg.Checkbox('', key='-NUMSNUMB-'), sg.Spin([i for i in range(1,30)], key='-NUMSNUMV-')],
        [sg.Checkbox('', key='-LOWNUMB-'), sg.Spin([i for i in range(1,30)], key='-LOWNUMV-')],
        [sg.Checkbox('', key='-UPNUMB-'), sg.Spin([i for i in range(1,30)], key='-UPNUMV-')],
        [sg.Checkbox('', key='-SPECNUMB-'), sg.Spin([i for i in range(1,30)], key='-SPECNUMV-')]]

layout = [[sg.T('Скрипт генерации паролей')],
        [sg.HSep()],
        [sg.T('Длина пароля:', size=(16,1)), sg.Spin([i for i in range(8,30)], initial_value=16, key='-LENSPIN-')],
        [sg.T('Количество паролей:', size=(16,1)), sg.Spin([i for i in range(1,30)], initial_value=10, key='-PASSNUM-')],
        [sg.HSep()],
        [sg.T('Настройка символов и их кол-ва')],
        [sg.Col(col1), sg.VSep(), sg.Col(col2)],
        [sg.HSep()],
        [sg.B('Генерировать'), sg.B('Выход')],
        [sg.Multiline('', size=(30, 10), key='-OUTPUT-')]]

window = sg.Window('Генератор паролей', layout)


while True:
    event, values = window.read()

    if event in (None, 'Выход'):
        break

    if not event == 'Генерировать':
        continue
    
    # Сборка настройки алфавита
    password_length = int(values['-LENSPIN-'])
    num_of_passwords = int(values['-PASSNUM-'])
    include_alph = [values['-NUMS-'], values['-LOWS-'], values['-UPPS-'], values['-SPEC-']]
    check_nums_bool = [values['-NUMSNUMB-'], values['-LOWNUMB-'], values['-UPNUMB-'], values['-SPECNUMB-']]
    check_nums_val = [values['-NUMSNUMV-'], values['-LOWNUMV-'], values['-UPNUMV-'], values['-SPECNUMV-']]
    check_conf = list(zip(check_nums_bool, check_nums_val))

    # Если ни один из символов не выбран
    if not any(include_alph):
        sg.PopupError('Вы не выбрали, какие символы включить в пароль', auto_close=True, auto_close_duration=5)
        continue
    
    # Проверка количества обязательных элементов
    if sum([check_nums_val[i] if check_nums_bool[i] else 0 for i in range(len(check_nums_val))]) > password_length:
        sg.PopupError('Количество обязательных элементов, выбранное вами, превышает длину пароля', auto_close=True, auto_close_duration=5)
        continue
    
    # Проверка самого пароля 
    pass_list = []
    generated = 0
    BREAKNUMBER = 1e4
    while len(pass_list) <= num_of_passwords:
        tmp_pass = create_password(include_alph, password_length)
        if check_password(tmp_pass, check_conf):
            pass_list.append(tmp_pass)
        window.refresh()
        generated += 1
        if generated > BREAKNUMBER:
            sg.PopupError(f'Возможно, вы ввели слишком сложные условия\nБыло сгенерировано {int(BREAKNUMBER)} паролей, не прошедших проверку\nПопробуйте поменять условия генерации', auto_close=True, auto_close_duration=5)
            break
    
    # Вывод сгенерированых паролей
    window['-OUTPUT-'].update('\n'.join(pass_list))


    



window.close()