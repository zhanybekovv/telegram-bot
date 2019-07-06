import telebot
import constants

bot = telebot.TeleBot(constants.token)
data = {'todo': '',
        'in_process': '',
        'done': ''}
data_user = {'users':
                 [{'username': 'kakimovaa',
                 'first_name': 'Aizada',
                 'last_name': 'Kakimova',
                 'score': '5'},
                  {'username': 'naukanove',
                   'first_name': 'Aldiyar',
                   'last_name': 'Naukanov',
                   'score': '5'},
                 {'username': 'janybekovn',
                   'first_name': 'Nartay',
                   'last_name': 'Zhanybekov',
                   'score': '5'}
                  ]}
string = ""
todo = ""
process = ""
done = ""
username = ""
score = ""

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("show todo")
    user_markup.row("save to todo")
    user_markup.row("in process")
    user_markup.row("done")
    user_markup.row("info")
    user_markup.row('grade')
    bot.send_message(message.chat.id, 'Choose', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if message.text == "save to todo":
        msg = bot.reply_to(message, "Какие у Вас планы на сегодня?")
        bot.register_next_step_handler(msg, todo_step)
    elif message.text == "in process":
        msg = bot.reply_to(message, "Что вы делаете?")
        bot.register_next_step_handler(msg, process_step)
    elif message.text == "show todo":
        show_todo_step(message)
    elif message.text == "done":
        msg = bot.reply_to(message, "Что вы уже сделали?")
        bot.register_next_step_handler(msg, done_step)
    elif message.text == "info":
        for i in range(len(data_user)+2):
            print(data_user['users'][i]['username'])
            user_markup.row(data_user['users'][i]['username'])
        msg = bot.reply_to(message, "О чьих достижениях Вы хотите узнать?", reply_markup=user_markup)
        bot.register_next_step_handler(msg, info_step)
    elif message.text == "grade":
        for i in range(len(data_user)+2):
            print(data_user['users'][i]['username'])
            user_markup.row(data_user['users'][i]['username'])
        user_markup.row('info')
        msg = bot.reply_to(message, "Кого Вы хотите оценить?", reply_markup=user_markup)
        bot.register_next_step_handler(msg, score_step)
    elif message.text == "back":
        handle_start(message)


def todo_step(message):
    global data, todo
    print("haha")
    print(message.text)
    todo = message.text
    data['todo'] = todo
    values = (str(todo))
    print(data)
    print(values)
    bot.send_message(message.chat.id, 'Добавлено! Удачного дня')


def show_todo_step(message):
    global string, todo, process, done
    string = ""
    todo = data['todo']
    process = data['in_process']
    done = data['done']
    if process == done:
        del process
        print(data)
        string = 'todo: ' + todo + " done: " + done
    elif todo == process:
        del todo
        print(data)
        string = 'todo: ' + ' process:' + process
    else:
        string = 'todo: ' + todo + ' process:' + process
    bot.send_message(message.chat.id, string)


def process_step(message):
    global string
    string = ""
    in_process = message.text
    data['in_process'] = in_process
    print("dg")
    print(data)
    string = in_process
    bot.send_message(message.chat.id, 'Добавлено! Удачного дня')


def done_step(message):
    global string, done
    string = ""
    done = message.text
    data['done'] = done
    print("done")
    print(data)
    string = done
    bot.send_message(message.chat.id, 'Добавлено! Удачного дня')


def info_step(message):
    global string, username, score
    username = message.text
    if data_user:
        for i in range(len(data_user)+2):
            print(data_user['users'][i]['username'])
if data_user['users'][i]['username'] == username:
                print('s')
                string = 'Информация о пользователе ' + data_user['users'][i]['first_name'] + " " + data_user['users'][i]['last_name'] + ':\n Средний балл: ' + str(score)
                bot.send_message(message.chat.id, string)
    else:
        bot.send_message(message.chat.id, 'Нету в базе такого пользователя:(')


def score_step(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    global string, username, score
    username = message.text
    if data_user:
        for i in range(len(data_user) + 2):
            if data_user['users'][i]['username'] == username:
                print('df')
            msg = bot.reply_to(message, "Сколько Вы ему поставите?", reply_markup=user_markup)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("1")
            user_markup.row("2")
            user_markup.row("3")
            user_markup.row("4")
            user_markup.row("5")
            user_markup.row("back")
            bot.send_message(message.chat.id, 'По 5-бальной шкале', reply_markup=user_markup)
            bot.register_next_step_handler(msg, grade_step)
            return i


def grade_step(message):
    global score
    score1 = message.text
    print('s')
    print(score1)
    if data_user:
        for i in range(len(data_user) + 2):
            print(data_user['users'][i]['score'])
            user_score = data_user['users'][i]['score']
            score = (float(user_score) + float(score1))/2
            print(score)
            return score


bot.polling(none_stop=True, interval=1)
