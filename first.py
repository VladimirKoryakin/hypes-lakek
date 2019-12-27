import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random


with open('C:/Users/user/Desktop/Hackathon27.12.19/hypes-lakek/token.txt', 'r') as file:
    token = file.readline()
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def create_keyb1(buttons):
    keyboard = VkKeyboard(one_time=True)
    for b in buttons:
        if b == 'new_line':
            keyboard.add_line()
        else:
            keyboard.add_button(b, color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
    if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        print(event.user_id)
        bred = True
        users = {}
        if event.user_id not in users:
            users[event.user_id] = 0
        if text == 'начать' or text == 'help':
            bred = False
            vk.messages.send(user_id=event.user_id,
                             random_id=random.randint(1, 10 ** 9),
                             message='Привет! Я чат-бот дня самоуправления. Если ты еще не зарегистрирровался,' +
                                     'то скорее нажимай на кнопку и присоединяйся к нам.',
                             keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
        elif text == 'расписание':
            vk.messages.send(user_id=event.user_id,
                             random_id=random.randint(1, 10 ** 9),
                             message='расписание',
                             keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
        if bred:
            vk.messages.send(user_id=event.user_id,
                             random_id=random.randint(1, 10 ** 9),
                             message='Извините, я Вас не понимаю(',
                             keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
