import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import google123

with open('C:/Users/user/Desktop/Hackathon27.12.19/hypes-lakek/token.txt', 'r') as file:
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


def sign_in(orig_event, number=1):
	questions = ['Сейчас я задам вам несколько вопросов. Как вас зовут(фамилия и имя)?',
		'Кем вы будете на день самоуправления(учитель или ученик)?',
		'Какой предмет вы собираетесь вести?',
		'Вы ' + users[orig_event.user_id][1].upper() + ' и вы ' + users[orig_event.user_id][2] + '?',
		'Вы зарегестрированы']
	if users[orig_event.user_id][0] == 1:
		vk.messages.send(user_id=orig_event.user_id,
						 random_id=random.randint(1, 10 ** 9),
						 message=questions[users[orig_event.user_id][0]],
						 keyboard=create_keyb1(['Учитель', 'Ученик']))
	elif users[orig_event.user_id][0] == 4:
		vk.messages.send(user_id=orig_event.user_id,
						 random_id=random.randint(1, 10 ** 9),
						 message=questions[users[orig_event.user_id][0]],
						 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
	else:
		vk.messages.send(user_id=orig_event.user_id,
			random_id=random.randint(1, 10 ** 9),
			message= questions[users[orig_event.user_id][0]])

	for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
		if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me:
			if users[event.user_id][0] == 4:
				return None
			if event.text.lower() == 'учитель':
				users[event.user_id][users[event.user_id][0] + 1] = event.text.lower()
				users[event.user_id][0] += 1
				sign_in(event, number=3)
				return

			text1 = event.text.lower()
			print(event.user_id)
			users[event.user_id][users[event.user_id][0] + 1] = text1
			users[event.user_id][0] += 1
			if text1 == 'ученик':
				users[event.user_id][0] += 1
			sign_in(event, number=users[event.user_id][0])

reg = False
users = {}
admins = {'305875074'}
for event in vk_api.longpoll.VkLongPoll(vk_session).listen():
	if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW and event.to_me:
		text = event.text.lower()
		print(event.user_id)
		bred = True
		if event.user_id not in users:
			users[event.user_id] = [0, '', '', '', '']
			print(event.user_id)
			print(users)
		if str(event.user_id) not in admins:
			if text == 'начать' or text == 'help':
				bred = False
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message='Привет! Я чат-бот дня самоуправления. Если ты еще не зарегистрирровался,' +
										 'то скорее нажимай на кнопку и присоединяйся к нам.',
								 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
			elif text == 'расписание':
				bred = False
				s = google123.whole_timetable(['5', '6', '7', '8', '10'])
				ans = ''
				for e in s:
					ans += e + ': ' + '\n'
					for h in s[e]:
						ans += str(h) + '. ' + s[e][h] + '\n'
					ans += '\n'
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message=ans,
								 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
			elif text == 'регистрация':
				sign_in(event)
				google123.add_user(users[event.user_id][1:-1])
				bred = False
				reg = True
			if bred and not reg:
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message='Извините, я Вас не понимаю(',
								 keyboard=create_keyb1(['Регистрация', 'Расписание', 'help']))
		else:
			if text == 'начать' or text == 'help':
				bred = False
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message='Привет! Я чат-бот дня самоуправления. Вам повезло: Вы есть в моем спике админов, скорее всего Вы являетесь организатором мероприятия.',
								 keyboard=create_keyb1(['Расписание', 'Кто уже зарегистрировался?', 'help']))
			elif text == 'расписание':
				bred = False
				s = google123.whole_timetable(['5', '6', '7', '8', '10'])
				ans = ''
				for e in s:
					ans += e + ': ' + '\n'
					for h in s[e]:
						ans += str(h) + '. ' + s[e][h] + '\n'
					ans += '\n'
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message=ans,
								 keyboard=create_keyb1(['Расписание', 'Кто уже зарегистрировался', 'help']))
			elif text == 'кто уже зарегистрировался':
				bred = False
				s = google123.get_users()
				print(s)
				ans = ''
				for e in s:
					for k in e:
						if e[k] != '':
							ans += e[k] + ';  '
					ans = ans[:-2]
					ans += '\n'
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message=ans,
								 keyboard=create_keyb1(['Расписание', 'Кто уже зарегистрировался', 'help']))
			if bred:
				vk.messages.send(user_id=event.user_id,
								 random_id=random.randint(1, 10 ** 9),
								 message='Извините, я Вас не понимаю(',
								 keyboard=create_keyb1(['Расписание', 'Кто уже зарегистрировался', 'help']))
