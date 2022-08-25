import datetime
import requests
from config import weather_key, telegram_key
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=telegram_key)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_key}&units=metric"
        )
        data = r.json()

        city = data["name"]
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = ' '
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        wind_deg_int = data["wind"]["deg"]
        if wind_deg_int == 0:
            wind_deg_str = 'Северный\U00002B06'
        if wind_deg_int == 360:
            wind_deg_str = 'Северный\U00002B06'
        elif (wind_deg_int > 0) and (wind_deg_int < 90):
            wind_deg_str = 'Северо-восточный\U00002197'
        elif wind_deg_int == 90:
            wind_deg_str = 'Восточный\U000027A1'
        elif (wind_deg_int > 90) and (wind_deg_int < 180):
            wind_deg_str = 'Юго-восточный\U00002198'
        elif wind_deg_int == 180:
            wind_deg_str = 'Южный\U00002B07'
        elif (wind_deg_int > 180) and (wind_deg_int < 270):
            wind_deg_str = 'Юго-западный\U00002199'
        elif wind_deg_int == 270:
            wind_deg_str = 'Западный\U00002B05'
        else:
            wind_deg_str = 'Северо-западный\U00002196'
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M')
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M')
        lengh_day_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                         datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"Сегодня: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n{wd}\n"
                            f'Погода в городе {city}:\nТемпература: {temperature} °C\U0001F321 \n'
                            f'Влажность: {humidity}%\U0001F4A7\nДавление: {pressure} мм.рт.ст.\n'
                            f'Скорость ветра: {wind_speed} м/с\U0001F4A8\nНаправление ветра: {wind_deg_str}\n'
                            f'Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\n'
                            f'Продолжительность светового дня: {lengh_day_time}')

    except:
        await message.reply("\U0000274C Неверное название города! \U0000274C")

if __name__ == '__main__':
    executor.start_polling(dp)
