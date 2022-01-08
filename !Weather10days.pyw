'''
Оконная программа-виджет для погоды
Захардкодил сюда сайт со своим прогнозом, но в принципе другие города на сайте тоже есть 

DATE: 08.01.2022
AUTHOR: Alex Akinin
'''
# TODO: Исключения, когда нет подключения к интернету -> всплывающее окно

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

from tkinter import font
import bs4
import requests as req
import PySimpleGUI as sg
import time

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

def get_gismeteo_data():
    weather_url = 'https://www.gismeteo.ru/weather-nizhny-novgorod-4355/10-days/'

    # Генераторы однотипных css селекторов
    css_selector_up = [f'.widget-row-chart-temperature > div:nth-child(1) > div:nth-child(2) > div:nth-child({i}) > div:nth-child(1) > span:nth-child(1)' for i in range(1,11)]
    css_selector_low = [f'.widget-row-chart-temperature > div:nth-child(1) > div:nth-child(2) > div:nth-child({i}) > div:nth-child(2) > span:nth-child(1)'for i in range(1,11)]
    css_selector_date = [f'.widget-menu-wrap > div:nth-child(1) > div:nth-child(1) > a:nth-child({i}) > div:nth-child(2)' for i in range(1,11)]
    css_selector_desc = [f'.widget-row-icon > div:nth-child({i}) > div:nth-child(1)' for i in range(1,11)]

    # Строка чтоб не подумали, что я бот (не уверен, что это так работет - с яндексом не прокатило)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    # Преобразование страницы в объект BeautifulSoup
    request_res = req.get(weather_url, headers=headers, )
    request_res.raise_for_status()
    bs_object = bs4.BeautifulSoup(request_res.text, 'html.parser')

    # Выжимка из страницы
    dates = [bs_object.select(selector)[0].getText() for selector in css_selector_date]
    max_temp = [bs_object.select(selector)[0].getText() for selector in css_selector_up]
    min_temp = [bs_object.select(selector)[0].getText() for selector in css_selector_low]
    descriptions = [bs_object.select(selector)[0].get('data-text') for selector in css_selector_desc]

    return list(zip(dates, max_temp, min_temp, descriptions))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

def col_lay(key_num):
    pad=((0,0), (0,0))
    return [[sg.Text('aa', key=f'-DATE{key_num}-', pad=pad, font='Any 16', size=(5,1))], 
    [sg.HSep()],
    [sg.T('', key=f'-MAXTEMP{key_num}-', pad=pad, font='Any 10', size=(5,1))], 
    [sg.T('', key=f'-MINTEMP{key_num}-', pad=pad, font='Any 10', size=(5,1))], 
    [sg.T('', key=f'-DES{key_num}-', pad=pad, font='Any 8', size=(10,3))]]

def VSep1():
    return sg.VSep(pad=((0,0), (0,0)))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

layout = [[sg.B('Обновить'), sg.B('Выход'), sg.T('UPD:', key='-LASTUPD-', size=(25,1))],
        [sg.Col(col_lay(1)), VSep1(), sg.Col(col_lay(2)), VSep1(), sg.Col(col_lay(3)), VSep1(), 
        sg.Col(col_lay(4)), VSep1(), sg.Col(col_lay(5)), VSep1(), sg.Col(col_lay(6)), VSep1(), 
        sg.Col(col_lay(7)), VSep1(), sg.Col(col_lay(8)), VSep1(), sg.Col(col_lay(9)), VSep1(), sg.Col(col_lay(10))]]

window = sg.Window('My Weather', layout, no_titlebar=True, grab_anywhere=True, alpha_channel=0.8)

last_update = 0 

while True:
    event, values = window.read(timeout=500, timeout_key='-TIMEOUT-')

    if event in (None, 'Выход'):
        break

    if event == '-TIMEOUT-':
        window.UnHide()
    
    if abs(time.time() - last_update) > 3600 or event == 'Обновить':
        weather_data = get_gismeteo_data()
        for i in range(10):
            window[f'-DATE{i+1}-'].update(weather_data[i][0])
            window[f'-MAXTEMP{i+1}-'].update(weather_data[i][1])
            window[f'-MINTEMP{i+1}-'].update(weather_data[i][2])
            window[f'-DES{i+1}-'].update(weather_data[i][3])
        last_update = time.time()
        print(time.ctime(time.time()))
        window['-LASTUPD-'].update(f'UPD: {time.ctime(time.time())}')


window.close()