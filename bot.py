import telebot
import constants

bot = telebot.TeleBot(constants.token)
data = {'todo': '',
        'in_process': '',
        'done': ''}
string = ""
todo = ""
process = ""
done = ""
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("show todo")
    user_markup.row("save to todo")
    user_markup.row("in process")
    user_markup.row("done")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "save to todo":
        msg = bot.reply_to(message, "Какие у Вас планы на сегодня?")
        bot.register_next_step_handler(msg, todo_step)
    if message.text == "in process":
        msg = bot.reply_to(message, "Что вы делаете?")
        bot.register_next_step_handler(msg, process_step)
    if message.text == "show todo":
        show_todo_step(message)
    if message.text == "done":
        msg = bot.reply_to(message, "Что вы уже сделали?")
        bot.register_next_step_handler(msg, done_step)


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

bot.polling(none_stop=True, interval=1)