import sqlite3

def get_more_informations(bot, call, filial, cours, cls):
    if filial == 0 or cours == 0 or cls == 0:
        bot.send_message(call.message.chat.id, "Ошибка, попробуйте заново выбрать сначала филиал, "
                                               "затем класс и курс")
    else:
        conn = sqlite3.connect('schedule.db')
        cur = conn.cursor()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='О ЧЕМ КУРС:', reply_markup=None)
        cur.execute(("select description from courses_description where name=? and class=?"), (cours, cls))
        rows = cur.fetchall()
        bot.send_message(call.message.chat.id, rows[0][0])
        conn.close()

def get_schedule(bot, call, filial, cours, cls):
    if filial == 0 or cours == 0 or cls == 0:
        bot.send_message(call.message.chat.id, "Ошибка, попробуйте заново выбрать сначала филиал, "
                                               "затем класс и курс")
    else:
        conn = sqlite3.connect('schedule.db')
        cur = conn.cursor()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    text='РАСПИСАНИЕ:', reply_markup=None)
        cur.execute(("select * from schedule inner join courses on schedule.id_subject=courses.id_subject "
                     "inner join filials f on courses.id_filial = f.id_filial "
                     "inner join courses_description c on courses.id_cours = c.id_cours where f.name=? and c.name=? and c.class=?"),
                    (filial, cours, cls))
        rows = cur.fetchall()
        if (rows == []):
            bot.send_message(call.message.chat.id, "Занятий нет")
        else:
            for row in rows:
                bot.send_message(call.message.chat.id, row[1] + '\n' + row[2])
        conn.close()

