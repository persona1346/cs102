import requests
import config
import telebot
from bs4 import BeautifulSoup
import datetime

bot = telebot.TeleBot(config.access_token)
telebot.apihelper.proxy = {'https': 'socks5h://194.190.170.38:82'}

days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_weekday(web_page, n):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день недели
    schedule_table = soup.find("table", attrs={"id": str(n) + "day"})

    if schedule_table is None:
        return None
    else:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        return times_list, locations_list, lessons_list

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group = message.text.split()
    n = days.index(day[1:]) + 1
    web_page = get_page(group)
    if parse_schedule_for_a_weekday(web_page, n) is None:
        bot.send_message(message.chat.id, "отдыхай", parse_mode='HTML')
    else:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_weekday(web_page, n)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    now = datetime.datetime.now()
    day, group = message.text.split()
    web_page = get_page(group)
    n = datetime.datetime.now().isoweekday()
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_weekday(web_page, n)
    fl = 0
    for i in range(len(times_lst)):
        today_static = now.replace(hour=int(times_lst[i][:2]), minute=int(times_lst[i][3:5]), second=0, microsecond=0)
        if now < today_static:
            fl = 1
            break
    if fl == 0:
        get_tommorow(message,near=True)
    else:
        resp = '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['tommorow'])
def get_tommorow(message,near=False):
    """ Получить расписание на следующий день """
    datetime.datetime.today()
    day, group = message.text.split()
    n = (datetime.datetime.today().weekday() + 1) % 7 + 1
    web_page = get_page(group)
    if parse_schedule_for_a_weekday(web_page, n) is None and near == True:
        n = 1
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_weekday(web_page, n)
        resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
    elif parse_schedule_for_a_weekday(web_page, n) is None:
        resp = "отдыхай"
    else:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_weekday(web_page, n)
        resp = ''
        if near:
            resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])

        else:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')



@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    day, group = message.text.split()
    web_page = get_page(group)
    for n in range(1, 8):
        print(n)
        if parse_schedule_for_a_weekday(web_page, n) is None:
            bot.send_message(message.chat.id, "отдыхай", parse_mode='HTML')
        else:
            times_lst, locations_lst, lessons_lst = \
                parse_schedule_for_a_weekday(web_page, n)
            resp = ''
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
