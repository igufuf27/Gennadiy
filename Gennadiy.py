import datetime as dt
import requests

DATABASE = {
    'Антон': 'Омск',
    'Саша': 'Москва',
    'Катя': 'Калининград',
    'Миша': 'Москва',
    'Дима': 'Челябинск',
    'Алина': 'Красноярск',
    'Егор': 'Пермь',
    'Коля': 'Красноярск',
    'Артём': 'Владивосток',
    'Петя': 'Михайловка'
}

UTC_OFFSET = {
    'Москва': 3,
    'Санкт-Петербург': 3,
    'Новосибирск': 7,
    'Екатеринбург': 5,
    'Нижний Новгород': 3,
    'Казань': 3,
    'Челябинск': 5,
    'Омск': 6,
    'Самара': 4,
    'Ростов-на-Дону': 3,
    'Уфа': 5,
    'Красноярск': 7,
    'Воронеж': 3,
    'Пермь': 5,
    'Волгоград': 3,
    'Краснодар': 3,
    'Калининград': 2,
    'Владивосток': 10
}


def format_count_friends(count_friends):
    if count_friends == 1:
        return '1 друг'
    elif 2 <= count_friends <= 4:
        return f'{count_friends} друга'
    else:
        return f'{count_friends} друзей'


def what_time(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime("%H:%M")
    return f_time


def what_weather(city):
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return '<сетевая ошибка>'
    if response.status_code == 200:
        return response.text.strip()
    else:
        return '<ошибка на сервере погоды>'


def process_Gennadiy(query):
    if query == 'сколько у меня друзей?':
        count_string = format_count_friends(len(DATABASE))
        return f'У тебя {count_string}'
    elif query == 'кто все мои друзья?' or query == 'кто мои друзья?' :
        friends_string = ', '.join(DATABASE.keys())
        return f'Твои друзья: {friends_string}'
    elif query == 'где все мои друзья?' or query == 'где мои друзья?':
        unique_cities = set(DATABASE.values())
        cities_string = ', '.join(unique_cities)
        return f'Твои друзья в городах: {cities_string}'
    else:
        return '<неизвестный запрос>'


def process_friend(name, query):
    if name in DATABASE:
        city = DATABASE[name]
        if query == 'ты где?':
            return f'{name} в городе {city}'
        elif query == 'который час?':
            if city not in UTC_OFFSET:
                return f'<не могу определить время в городе {city}>'
            time = what_time(city)
            return f'Там сейчас {time}'
        elif query == 'как погода?':
            weather = what_weather(city)
            return weather
        else:
            return '<неизвестный запрос>'
    else:
        return f'У тебя нет друга по имени {name}'


def process_query(query):
    tokens = query.split(', ')
    if len(tokens) < 2:
        return '<неверный запрос>'
    name = tokens[0]
    if name == 'Геннадий':
        return process_Gennadiy(tokens[1])
    else:
        return process_friend(name, tokens[1])

print("""Привет! Я помощник Геннадий.
Конечно, моя сестра Алиса в своем деле преуспела больше, но и я смогу тебе кое-чем помочь...
Спроси у меня, кто твои друзья! Также я подскажу, сколько у тебя друзей, где твои друзья =)
Кроме того, через меня ты можешь узнать, как погода, который час, где твои друзья...
PS. Обращайся ко мне по имени. \nЕсли спрашиваешь про конкретного друга, обращайся ко мне по его имени.
""")

query = input("Введи свой вопрос: ")
request_number = 1

while query != "Стоп" and query != "стоп" and query != "остановись" and query != "Господин, это все":
    if request_number == 1:
        print(process_query(query))
        request_number += 1
    elif request_number < 5:
        query = input("ВВеди следующий запрос: ")
        print(process_query(query))
        request_number += 1  
    elif request_number < 20:
        if request_number % 3 == 0: 
            print ("Ты можешь спросить Антона: ты где? как погода? который час?")
        elif request_number % 5 == 0:
            print ("Если ты устал, введи стоп")
        query = input("ВВеди следующий запрос: ")
        print(process_query(query))
        request_number += 1
    else:
        print("Прости, теперь я устал.")
        break
print("Приятно было поболтать, чао, амиго!")
input()
