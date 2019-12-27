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
        vk.messages.send(user_id=event.user_id,
                          random_id=random.randint(1, 10 ** 9),
                          message='Привет!', keyboard=create_keyb1(['Здарова!', 'Hi!']))
