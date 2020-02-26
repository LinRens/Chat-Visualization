import json
import datetime

with open('dialog_tg.json', encoding='UTF-8') as file:
    data = json.load(file)

messages = data['chats']
messages = messages['list']
messages.pop(0)
chat_tg = messages[0]
chat_tg.pop('id')

chat_tg = chat_tg.get('messages')


all_photos_tg = 0     # количество фотографий
all_additional_tg = 0  # количество пересланных сообщений
calls_tg = 0          # количество звонков
calls_duration = 0    # общая продолжительность
voice = 0             # количество голосовых сообщений
voice_duration = 0    # общая продолжительность голосовых сообщений

for message in chat_tg:
    if type(message['text']) != str:
        chat_tg.remove(message)

for message in chat_tg:
    if type(message['text']) != str:
        chat_tg.remove(message)

for message in chat_tg:
    index = chat_tg.index(message)
    if message.get('from') == 'Veir Rocky':
        message['from'] = 'Лин'

for message in chat_tg:
    if 'action' in message:
        calls_tg += 1
        if 'duration_seconds' in message:
            calls_duration += message['duration_seconds']
        chat_tg.remove(message)

for message in chat_tg:
    if 'action' in message:
        chat_tg.remove(message)

for message in chat_tg:
    if 'reply_to_message_id' in message:
        all_additional_tg += 1

for message in chat_tg:
    if 'photo' in message:
        all_photos_tg += 1

for message in chat_tg:
    if 'file' in message:
        if 'media_type' in message:
            if message['media_type'] == 'voice_message':
                voice+= 1
                voice_duration += message['duration_seconds']

for message in chat_tg:
    if message.get('from') == 'Veir Rocky': # это мы изменили имя
        message['from'] = 'Лин'

for message in chat_tg:
    date = message['date']
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
    message['date'] = date

for message in chat_tg:
    index = chat_tg.index(message)
    right_message = {'date': message['date'], 'from': message['from'],
                     'len_message': len(message['text']), 'text': message['text']}
    chat_tg[index] = right_message
