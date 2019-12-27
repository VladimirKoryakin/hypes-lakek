import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random


with open('/home/annushka/hypes-lakek/token.txt', 'r') as file:
	token1 = file.readline()
	print(token1)
vk_session = vk_api.VkApi(token=token1)
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

users = {}

for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
	if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me:
		text = event.text.lower()
		print(event.user_id)
		bred = True
		if event.user_id not in users:
			users[event.user_id] = [0, '', '', '']
		if text == 'начать' or text == 'help':
			bred = False
			vk.messages.send(user_id=event.user_id,
							 random_id=random.randint(1, 10 ** 9),
							 message='Привет! Я чат-бот дня самоуправления. Если ты еще не зарегистрирровался,' +
									 'то скорее нажимай на кнопку и присоединяйся к нам.',
							 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
		elif text == 'расписание':
			bred = False
			vk.messages.send(user_id=event.user_id,
							 random_id=random.randint(1, 10 ** 9),
							 message='расписание',
							 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))

		elif text == 'регистрация':
			sign_in(event)
			bred = False
			
		if bred:
			vk.messages.send(user_id=event.user_id,
							 random_id=random.randint(1, 10 ** 9),
							 message='Извините, я Вас не понимаю(',
							 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))


def sign_in(orig_event, number=1):
	questions = ['Сейчас я задам вам несколько вопросов. Как вас зовут(фамилия и имя)?',
		'Кем вы будете на день самоуправления(учитель или ученик)?',
		'Какой предмет вы собираетесь вести?',
		'Вы ' + users[orig_event.user_id][1] + ' и вы ' + users[orig_event.user_id][2] + '?', 
		'Вы зарегестрированы']
	users[orig_event.user_id] = 0
	vk.messages.send(user_id=orig_event.user_id,
		random_id=random.randint(1, 10 ** 9),
		message= questions[users[orig_event.user_id]],
		keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))

	for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
		if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me:
			if users[event.user_id][0] == 4:
				return None
			if event.text.lower() == 'учитель':
				users[[event.user_id][users[event.user_id][0]]] = event.text.lower()
				sign_in(number=3)
			text = event.text.lower()
			print(event.user_id)
			users[[event.user_id][users[event.user_id][0]]] = event.text.lower()
			users[event.user_id][0] += 1
			sign_in(event, number=users[event.user_id][0])
			