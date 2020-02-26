import numpy as np
import pandas as pd
from itertools import groupby
from parser_vk import chat_vk, all_photos_vk
from parser_tg import chat_tg, all_photos_tg

len_vk = len(chat_vk)
len_tg = len(chat_tg)

dataset = chat_tg + chat_vk

lin_messages = []
tim_messages = []

for message in dataset:
    if message.get('from') == 'Лин':
        lin_messages.append(message)
    elif message.get('from') == 'Тим':
        tim_messages.append(message)

# строки по автору
lin_string = ''
for message in lin_messages:
    lin_string = lin_string + message['text'] + ' '
while '\\n' in lin_string:
    lin_string.replace('\\n', ' ')

tim_string = ''
for message in tim_messages:
    tim_string = tim_string + message['text'] + ' '
while '\\n' in tim_string:
    tim_string.replace('\\n', ' ')

all_dates = []
for message in dataset:
    all_dates.append(message['date'])

all_dates = set(all_dates)
all_dates = list(all_dates)
all_dates = sorted(all_dates)

data_frame = {x: 0 for x in all_dates}

# словарь вида дата: количество сообщений в дату
for message in dataset:
    data_frame[message['date']] += 1

data_frame_lin = {x: 0 for x in all_dates}
for message in dataset:
    if message['from'] == 'Лин':
        data_frame_lin[message['date']] += 1

data_frame_tim = {x: 0 for x in all_dates}
for message in dataset:
    if message['from'] == 'Тим':
        data_frame_tim[message['date']] += 1

frame_lin_nums = []
for date in all_dates:
    frame_lin_nums.append(data_frame_lin[date])

frame_tim_nums = []
for date in all_dates:
    frame_tim_nums.append(data_frame_tim[date])

frame_all_nums = []
for date in all_dates:
    frame_all_nums.append(data_frame[date])

df1 = {'all': np.array(frame_all_nums),
       'Lin': np.array(frame_lin_nums),
       'Tim': np.array(frame_tim_nums)}

df1 = pd.DataFrame(df1, index=all_dates)


unique_months = []
for date in all_dates:
    unique_months.append([date.month, date.year])

unique_months = [el for el, _ in groupby(unique_months)] # удалили повторы. теперь список сортирован и уникален

months = ["Январь", "Февраль", "Март", "Апрель", "Май", 'Июнь', "Июль", "Август",
         "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

months_and_nums = {i+1: months[i] for i in range(len(months))}
indexes = [str(months_and_nums[i[0]])+' ' + str(i[1]) for i in unique_months]
months_dataset = []

data_frame_months = {x: 0 for x in indexes}

# словарь вида месяц, год : количество сообщений в этот месяц
for element in data_frame:
    data_frame_months[str(months_and_nums[element.month]) + ' ' + str(element.year)] += data_frame[element]
max_all = max(data_frame_months.values())

# по авторам
data_frame_months_lin = {x: 0 for x in indexes}
for element in data_frame_lin:
    data_frame_months_lin[str(months_and_nums[element.month]) + ' ' + str(element.year)] += data_frame_lin[element]
max_lin = max(data_frame_months_lin.values())


data_frame_months_tim = {x: 0 for x in indexes}
for element in data_frame_tim:
    data_frame_months_tim[str(months_and_nums[element.month]) + ' ' + str(element.year)] += data_frame_tim[element]
max_tim = max(data_frame_months_tim.values())


data_frame_months = data_frame_months.values()
data_frame_months = list(data_frame_months)

data_frame_months_lin = data_frame_months_lin.values()
data_frame_months_lin = list(data_frame_months_lin)

data_frame_months_tim = data_frame_months_tim.values()
data_frame_months_tim = list(data_frame_months_tim)


df_months = {'all': np.array(data_frame_months),
             'Lin': np.array(data_frame_months_lin),
             'Tim': np.array(data_frame_months_tim)}
df_months = pd.DataFrame(df_months, index=indexes)


len_messages = []
for message in dataset:
    len_messages.append(message['len_message'])


print("{} - {}".format(len(all_dates), 'всего дней переписки'))
print("{} - {}".format(len(lin_messages), 'сообщений от меня'))
print("{} - {}".format(len(tim_messages), 'сообщений от тебя'))
print("{} - {}".format(len(lin_string), 'знаков от меня'))
print("{} - {}".format(len(tim_string), 'знаков от тебя'))
print("{} - {}".format(len(tim_string + lin_string), 'знаков всего'))
print("{} - {}".format(all_photos_tg, 'фотографий из Telegram'))
print("{} - {}".format(all_photos_vk, 'фотографий из ВКонтакте'))
print("{} - {}".format(len_vk, 'сообщений из ВКонтакте'))
print("{} - {}".format(len_tg, 'сообщений из Телеграма'))
print("{} - {}".format(len(dataset), 'всего сообщений'))
