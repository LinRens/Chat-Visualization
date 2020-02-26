import os
from bs4 import BeautifulSoup
import datetime

chat_vk = []

months_nums = {'янв': 1, 'фев': 2, 'мар': 3, "апр": 4, "мая": 5, "июн": 6,
               'июл': 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12}

all_audios_vk = 0  # сколько аудиозаписей
all_calls_vk = 0  # сколько звонков
all_additional_vk = 0  # сколько прикрепленных
all_walls_vk = 0  # сколько записей на стене
all_photos_vk = 0  # количество фотографий

dir_name = "vk_chat"
test = os.listdir(dir_name)

for item in test:
    with open('vk_chat\\' + item, "r") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')

    divs = soup.find_all('div', {'class': 'message'})

    data = []

    for div in divs:
        message = div.text.strip()
        data.append(message)

    for j in range(len(data)):
        data[j] = data[j].split('\n')

    # список всех сообщений. с автором, текстом, датой и чем-то еще.

    audios_vk = 0  # сколько аудиозаписей
    calls_vk = 0  # сколько звонков
    additional_vk = 0  # сколько прикрепленных
    walls_vk = 0  # сколько отправленных записей
    photos_vk = 0  # количество фотографий
    chat_list = []

    for message in data:

        message_info = {}
        index = data.index(message)

        if 'Фотография' in message:
            photos_vk += 1
            photo_index = message.index('Фотография')
            message[photo_index:] = []

        if 'Запись на стене' in message:
            walls_vk += 1

        if 'Звонок' in message:
            calls_vk += 1
        if 'Аудиозапись' in message:
            audios_vk += 1

        # разделим имя и дату на отдельные сообщения

        little_list = message[0].split(', ')
        message.pop(0)
        message.insert(0, little_list[0])
        message.insert(1, little_list[1])
        # даты в адекватный формат
        message_list = message[1].split(' ')
        message_list = message_list[0:3]
        message_list[1] = months_nums[message_list[1]]
        date = datetime.date(int(message_list[2]), int(message_list[1]), int(message_list[0]))

        # имена
        if message[0] == 'Вы':
            message[0] = 'Лин'
        elif message[0] == 'Тимофей Лебедев':
            message[0] = 'Тим'

        message_info['date'] = date
        message_info['text'] = message[2]
        message_info['len_message'] = len(message_info['text'])
        message_info['from'] = message[0]
        chat_list.append(message_info)

    chat_vk = chat_vk + chat_list
    all_audios_vk = all_audios_vk + audios_vk
    all_calls_vk = all_calls_vk + calls_vk
    all_additional_vk = all_additional_vk + additional_vk
    all_walls_vk = all_walls_vk + walls_vk
    all_photos_vk = all_photos_vk + photos_vk
