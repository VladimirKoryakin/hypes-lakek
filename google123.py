import gspread
from oauth2client.service_account import ServiceAccountCredentials


def timetable_for_class(class_, records):
	time = {}
	for i in records:
		time[i['']] = i[class_]
	return time


def whole_timetable(classes):
	scope = ['https://spreadsheets.google.com/feeds/', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('croc271219-e5838b0ab675.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open('timetable').sheet1
	records = sheet.get_all_records()
	time = {}
	for key in classes:
		time[key] = timetable_for_class(key, records)
	return time


def add_user(user):
    scope = ['https://spreadsheets.google.com/feeds/', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('croc271219-e5838b0ab675.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('timetable').get_worksheet(1)
    sheet.add_rows(1)
    sheet.append_row(user)


def get_users():
    scope = ['https://spreadsheets.google.com/feeds/', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('croc271219-e5838b0ab675.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('timetable').get_worksheet(1)
    records = sheet.get_all_records()
    return records
