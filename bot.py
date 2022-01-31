"""bot.py"""
import telebot
from telebot import types
import selecting

bot = telebot.TeleBot('1221374015:AAFztvwyiFF5anMyrSNabohu5HUbAhalzoc')

@bot.message_handler(commands=['help'])
def get_help(message):
    """get help"""
    bot.send_message(message.chat.id, "/help - информация о всех командах\n"
                                      "/contacts - контакты\n"
                                      "/menu - вернуться к выбору филиала")

@bot.message_handler(commands=['contacts'])
def get_contacts(message):
    """get contacts"""
    bot.send_message(message.chat.id, "Общий телефон для связи: +7 (495) 120-99-75\n\n"
                                      "Технопарк Инжинириум МГТУ им. Н. Э. Баумана (Нарвская)\n"
                                      "Адрес: ул. Нарвская, д. 1А, корп.3\n"
                                      "Телефон: \n"
                                      "Рабочее время: 10:00-18:00\n\n"
                                      "Технопарк Инжинириум МГТУ им. Н. Э. Баумана (Бауманская)\n"
                                      "Адрес: Госпитальный пер. 4/6 с.1\n"
                                      "Телефон: \n"
                                      "Рабочее время: 10:00-18:00")

@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    """get welcome message"""
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttom1 = types.KeyboardButton("Технопарк (Нарвская)")
    buttom2 = types.KeyboardButton("Технопарк (Бауманская)")
    menu.add(buttom1, buttom2)
    if message.text == '/start':
        bot.send_message(message.chat.id, "Привет! Выбери интересующий тебя филиал 'Инжинириум "
                                          "МГТУ им. Н.Э.Баумана'.\n\nДля того, чтобы узнать "
                                          "перечень команд, напиши '/help'", reply_markup=menu)
    else:
        bot.send_message(message.chat.id, "Выбери интересующий тебя филиал:",
                         reply_markup=menu)


COURSES = ["Программирование на Python", "Основы программирования на C++", "Веб-программирование"]
FILIAL, COURS, CLS, KLAVA = 0, 0, 0, 1

@bot.message_handler(content_types=['text'])
def get_message(message):
    """get text message"""
    global FILIAL, COURS, CLS, COURSES, KLAVA

    if message.text == 'Технопарк (Нарвская)' or message.text == 'Технопарк (Бауманская)':
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        buttom1 = types.KeyboardButton("5-8 класс")
        buttom2 = types.KeyboardButton("9-11 класс")
        buttom3 = types.KeyboardButton("Назад")
        menu.add(buttom1, buttom2, buttom3)
        bot.send_message(message.chat.id, "Выберите класс:", reply_markup=menu)

        if message.text == 'Технопарк (Нарвская)':
            FILIAL = "Технопарк (Нарвская)"
        else:
            FILIAL = "Технопарк (Бауманская)"

    elif message.text == '5-8 класс':
        CLS = "5-8"
        KLAVA = 2
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        buttom1 = types.KeyboardButton(COURSES[0] + " (5-8 класс)")
        buttom2 = types.KeyboardButton(COURSES[1] + " (5-8 класс)")
        buttom3 = types.KeyboardButton(COURSES[2] + " (5-8 класс)")
        buttom4 = types.KeyboardButton("Назад")
        menu.add(buttom1, buttom2, buttom3, buttom4)
        bot.send_message(message.chat.id, "Выберите курс:", reply_markup=menu)

    elif message.text == '9-11 класс':
        CLS = "9-11"
        KLAVA = 2
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        buttom1 = types.KeyboardButton(COURSES[0] + " (9-11 класс)")
        buttom2 = types.KeyboardButton(COURSES[1] + " (9-11 класс)")
        buttom3 = types.KeyboardButton("Назад")
        menu.add(buttom1, buttom2, buttom3)
        bot.send_message(message.chat.id, "Выберите курс:", reply_markup=menu)

    elif message.text == "Назад":
        if KLAVA == 1:
            menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttom1 = types.KeyboardButton("Технопарк (Нарвская)")
            buttom2 = types.KeyboardButton("Технопарк (Бауманская)")
            menu.add(buttom1, buttom2)
            bot.send_message(message.chat.id, "Выбери интересующий тебя филиал:",
                             reply_markup=menu)
        elif KLAVA == 2:
            menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttom1 = types.KeyboardButton("5-8 класс")
            buttom2 = types.KeyboardButton("9-11 класс")
            buttom3 = types.KeyboardButton("Назад")
            menu.add(buttom1, buttom2, buttom3)
            bot.send_message(message.chat.id, "Выберите класс:", reply_markup=menu)
            KLAVA = 1

    elif find_cours(message.text):
        inline = types.InlineKeyboardMarkup(row_width=1)
        buttom1 = types.InlineKeyboardButton("Узнать подробнее о курсе", callback_data="more")
        buttom2 = types.InlineKeyboardButton("Узнать расписание", callback_data="schedule")
        inline.add(buttom1, buttom2)
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=inline)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """callback function"""
    if call.data == 'more':
        selecting.get_more_informations(bot, call, FILIAL, COURS, CLS)
    elif call.data == 'schedule':
        selecting.get_schedule(bot, call, FILIAL, COURS, CLS)


def find_cours(mes):
    """check courses"""
    global COURS
    mes = mes.split(" (")
    for i in COURSES:
        if mes[0] == i:
            COURS = i
            return True
    return False


# запускаем бота
bot.polling(none_stop=True)
