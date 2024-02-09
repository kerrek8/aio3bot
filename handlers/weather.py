import json
import os
from datetime import datetime

import aiohttp
from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from keyboards.inline_keyboards.builder import inline_builder
from keyboards.reply_keyboards.builder import reply_builder
from misk.weather_misks import WeatherEndpointCurrent, WeatherEndpointDays, city_coords

load_dotenv()

router = Router()


@router.callback_query(F.data == 'start_weather')
async def weather(c: CallbackQuery):
    kb = await inline_builder(text=['Стрежевой', 'Тюмень', 'Текущее местоположение', 'Отмена'],
                              callback_data=['city_strej', 'city_tymen', 'curent_location', 'weather_cansel'],
                              sizes=[2, 1, 1])
    await c.answer()
    await c.message.answer("Выберите город", reply_markup=kb)


@router.callback_query(F.data == 'weather_cansel')
async def light_cansel(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text('Отменено', reply_markup=None)


@router.callback_query(F.data == 'curent_location')
async def curent_weather(c: CallbackQuery):
    await c.answer()
    kb = await reply_builder(text=['Отправить текущее местоположение'], send_loc=True)
    await c.message.answer('Нажмите на кнопкурядом с клавиатурой, чтобы отправить мне ваще текущее местоположение',
                           reply_markup=kb)


@router.message(F.location)
async def weather_by_location(m: Message):
    latitude = m.location.latitude
    longitude = m.location.longitude
    t = ['Сейчас', 'Сегодня', 'Завтра', 'Послезавтра']
    cd = ['wtime_' + 'Сейчас_' + f'{latitude}_{longitude}', 'wtime_' + '8_' +
          f'{latitude}_{longitude}',
          'wtime_' + '16_' + f'{latitude}_{longitude}', 'wtime_' + '35_' +
          f'{latitude}_{longitude}']
    t.append('На  5 дней')
    cd.append('wtime_40_' + f'{latitude}_{longitude}')
    t.append('Отмена')
    cd.append('weather_cansel')
    kb = await inline_builder(text=t, callback_data=cd, sizes=[1, 3, 1, 1])
    await m.answer('Выберите интересующую вас опцию', reply_markup=kb)


@router.callback_query(F.data.startswith('city_'))
async def get_option(c: CallbackQuery):
    data = c.data.split('_')[1]
    latitude = city_coords[data]['latitude']
    longitude = city_coords[data]['longitude']
    await c.answer()
    t = ['Сейчас', 'Сегодня', 'Завтра', 'Послезавтра']
    cd = ['wtime_' + 'Сейчас_' + f'{latitude}_{longitude}', 'wtime_' + '8_' +
          f'{latitude}_{longitude}',
          'wtime_' + '16_' + f'{latitude}_{longitude}', 'wtime_' + '35_' +
          f'{latitude}_{longitude}']
    t.append('На  5 дней')
    cd.append('wtime_40_' + f'{latitude}_{longitude}')
    t.append('Отмена')
    cd.append('weather_cansel')
    kb = await inline_builder(text=t, callback_data=cd, sizes=[1, 3, 1, 1])
    await c.message.edit_text('Выберите интересующую вас опцию', reply_markup=kb)


@router.callback_query(F.data.startswith('wtime_'))
async def weather(c: CallbackQuery):
    time = c.data.split('_')[1]
    latitude = c.data.split('_')[2]
    longitude = c.data.split('_')[3]
    if time == 'Сейчас':
        await now(c, latitude, longitude)
    elif time == '8':
        await today(c, latitude, longitude)
    elif time == '16':
        await tomorrow(c, latitude, longitude)
    elif time == '35':
        await aftertomorrow(c, latitude, longitude)
    elif time == '40':
        await fivedays(c, latitude, longitude)


async def now(c: CallbackQuery, latitude, longitude):
    data = await get_weather_now(latitude, longitude)
    if data['cod'] != 200:
        await c.answer()
        await c.message.edit_text("что-то пошло не так, попробуйте позже", reply_markup=None)
        print(data)
        return
    city = data['name']
    temp = round(data['main']['temp'] + 1)
    feels_like = round(data['main']['feels_like'] + 1)
    speed = data['wind']['speed']
    weather = data['weather'][0]['description']
    cloudnes = data['clouds']['all']
    s = f"🌤ПОГОДА В ГОРОДЕ {city} СЕЙЧАС🌤\n" \
        f"<b>Температура: {temp}°C</b>\n" \
        f"Ощущается: {feels_like}°C\n" \
        f"Погода: {weather}\n" \
        f"Облачность: {cloudnes}%\n" \
        f"Скорость ветра: {speed}м/с\n"
    await c.answer()
    await c.message.edit_text(s, parse_mode='html', reply_markup=None)


async def today(c: CallbackQuery, lat, lon):
    cnt = 8
    data = await get_weather_days(lat, lon, cnt)
    if data['cod'] != '200':
        await c.answer()
        await c.message.edit_text("что-то пошло не так, попробуйте позже", reply_markup=None)
        return
    d = data['list']
    city = data['city']['name']
    delta = int(int(data['city']['timezone']) / 3600)
    s = f'🌤ПОГОДА В ГОРОДЕ {city} НА СЕГОДНЯ (Время UTC+{delta})🌤\n' \
        f'🌤{d[0]["dt_txt"][8:10] + "-" + d[0]["dt_txt"][5:7] + "-" + d[0]["dt_txt"][0:4]}🌤\n'
    listtoappend = []
    for i in range(len(d)):
        timebrake = int(d[i]['dt_txt'][11:13])
        timebrake += delta
        if timebrake > 24:
            break
        h = [str(timebrake) + ':00', d[i]["main"]['temp'], d[i]['main']['feels_like'],
             d[i]['weather'][0]['description'], d[i]['clouds']['all']]
        listtoappend.append(h)
    for i in listtoappend:
        s = (s + f'\nВ {i[0]} \n' + f'<b>Температура: {round(i[1] + 1)}\n</b>' + f'Ощущается как: {round(i[2] + 1)}\n' +
             f'Погода: {i[3]}\n' + f'Облачность: {i[4]}%\n')
    await c.answer()
    await c.message.edit_text(s, parse_mode='html', reply_markup=None)


async def tomorrow(c: CallbackQuery, lat, lon):
    cnt = 16
    data = await get_weather_days(lat, lon, cnt)
    if data['cod'] != '200':
        await c.answer()
        await c.message.edit_text("что-то пошло не так, попробуйте позже", reply_markup=None)
        return
    d = data['list']
    city = data['city']['name']
    delta = int(int(data['city']['timezone']) / 3600)
    day = datetime.now().strftime('%d')
    while True:
        if int(d[0]['dt_txt'][8:10]) == int(day):
            del d[0]
        else:
            break
    s = f'🌤ПОГОДА В ГОРОДЕ {city} НА ЗАВТРА (Время UTC+{delta})🌤\n' \
        f'🌤{d[0]["dt_txt"][8:10] + "-" + d[0]["dt_txt"][5:7] + "-" + d[0]["dt_txt"][0:4]}🌤\n'
    listtoappend = []
    for i in range(len(d)):
        timebrake = int(d[i]['dt_txt'][11:13])
        timebrake += delta
        if timebrake > 24:
            break
        h = [str(timebrake) + ':00', d[i]["main"]['temp'], d[i]['main']['feels_like'],
             d[i]['weather'][0]['description'], d[i]['clouds']['all']]
        listtoappend.append(h)
    for i in listtoappend:
        s = (s + f'\nВ {i[0]} \n' + f'<b>Температура: {round(i[1] + 1)}\n</b>' + f'Ощущается как: {round(i[2] + 1)}\n' +
             f'Погода: {i[3]}\n' + f'Облачность: {i[4]}%\n')
    await c.answer()
    await c.message.edit_text(s, parse_mode='html', reply_markup=None)


async def aftertomorrow(c: CallbackQuery, lat, lon):
    cnt = 35
    data = await get_weather_days(lat, lon, cnt)
    if data['cod'] != '200':
        await c.answer()
        await c.message.edit_text("что-то пошло не так, попробуйте позже", reply_markup=None)
        return
    d = data['list']
    city = data['city']['name']
    delta = int(int(data['city']['timezone']) / 3600)
    day = datetime.now().strftime('%d')
    while True:
        if int(d[0]['dt_txt'][8:10]) == int(day) or int(d[0]['dt_txt'][8:10]) == int(day) + 1:
            del d[0]
        else:
            break
    s = f'🌤ПОГОДА В ГОРОДЕ {city} НА ПОСЛЕЗАВТРА (Время UTC+{delta})🌤\n' \
        f'🌤{d[0]["dt_txt"][8:10] + "-" + d[0]["dt_txt"][5:7] + "-" + d[0]["dt_txt"][0:4]}🌤\n'
    listtoappend = []
    for i in range(len(d)):
        timebrake = int(d[i]['dt_txt'][11:13])
        timebrake += delta
        if timebrake > 24:
            break
        h = [str(timebrake) + ':00', d[i]["main"]['temp'], d[i]['main']['feels_like'],
             d[i]['weather'][0]['description'], d[i]['clouds']['all']]
        listtoappend.append(h)
    for i in listtoappend:
        s = (s + f'\nВ {i[0]} \n' + f'<b>Температура: {round(i[1] + 1)}\n</b>' + f'Ощущается как: {round(i[2] + 1)}\n' +
             f'Погода: {i[3]}\n' + f'Облачность: {i[4]}%\n')
    await c.answer()
    await c.message.edit_text(s, parse_mode='html', reply_markup=None)


async def fivedays(c: CallbackQuery, lat, lon):
    cnt = 40
    data = await get_weather_days(lat, lon, cnt)
    if data['cod'] != '200':
        await c.answer()
        await c.message.edit_text("что-то пошло не так, попробуйте позже", reply_markup=None)
        return
    d = data['list']
    city = data['city']['name']
    delta = int(int(data['city']['timezone']) / 3600)
    s = f'🌤ПОГОДА В ГОРОДЕ {city} НА 5 ДНЕЙ (Время UTC+{delta})🌤\n' \
        f'🌤{d[0]["dt_txt"][8:10] + "-" + d[0]["dt_txt"][5:7] + "-" + d[0]["dt_txt"][0:4]}🌤\n'
    listtoappend = []
    for i in range(len(d)):
        timebrake = int(d[i]['dt_txt'][11:13])
        timebrake += delta
        if timebrake > 24:
            continue
        date = f'{d[i]["dt_txt"][8:10]}-{d[i]["dt_txt"][5:7]}-{d[i]["dt_txt"][0:4]}'
        h = [date, str(timebrake) + ':00', d[i]["main"]['temp'], d[i]['main']['feels_like'],
             d[i]['weather'][0]['description'], d[i]['clouds']['all']]
        listtoappend.append(h)
    for i in listtoappend:
        if i[1] == '7:00' or i[1] == '5:00':
            s = (s + f'\n🌤{i[0]}🌤\n' + f'\nВ {i[1]} \n' + f'<b>Температура: {round(i[2] + 1)}\n</b>' +
                 f'Ощущается как: {round(i[3] + 1)}\n' + f'Погода: {i[4]}\n' + f'Облачность: {i[5]}%\n')
        else:
            s = (s + f'\nВ {i[1]} \n' + f'<b>Температура: {round(i[2] + 1)}\n</b>' +
                 f'Ощущается как: {round(i[3] + 1)}\n' + f'Погода: {i[4]}\n' + f'Облачность: {i[5]}%\n')
    await c.answer()
    await c.message.edit_text(s, parse_mode='html', reply_markup=None)


async def get_weather_days(latitude, longitude, cnt) -> dict:
    url = await WeatherEndpointDays()
    url = url.format(latitude, longitude, cnt, os.getenv("OWM_API"))

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()
    data = json.loads(r)
    return data


async def get_weather_now(latitude, longitude) -> dict:
    url = await WeatherEndpointCurrent()
    url = url.format(latitude, longitude, os.getenv("OWM_API"))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()
    data = json.loads(r)
    return data
