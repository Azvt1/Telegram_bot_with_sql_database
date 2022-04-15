import telebot

from Telegram_bot_SQL.constant import admin_id
from Telegram_bot_SQL.db_functions import *

bot = telebot.TeleBot("5358815088:AAEfaA9KB2GRvTypeAvimPn3XHg6lwbDBYo")

def log(message):
    print("\n ------------")
    from datetime import datetime
    date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    text = ("Сообщение от {0} {1}.(id = {2}) \n Текст - {3}".format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                    str(message.from_user.id), message.text))
    f = open("../zapis_userov.txt", 'a', encoding='utf-8')
    f.write("\n\n" + date + " " + text)
    f.close()


respawn = ''
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id == admin_id:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        user_markup.row('/add_restaurant', '/remove_restaurant', '/edit_restaurant')
        user_markup.row('/add_food_type', '/remove_food_type', '/edit_food_type')
        user_markup.row('/add_food', '/remove_food', '/edit_food')
        bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, 'Извини, но тебе сюда нельзя ;d')


@bot.message_handler(commands='add_restaurant')
def add_restaurant(message):
    global respawn
    respawn = 'add_restaurant'
    bot.send_message(message.from_user.id, "Введите имя и адрес ресторана: Имя/Адресс")


@bot.message_handler(commands='edit_restaurant')
def editing_restaurant(message):
    global respawn
    respawn = 'edit_restaurant'

    text = ''
    restaurants = get_all_restaurants()
    for restaurant in restaurants:
        text += str(restaurant[0]) + ") " + restaurant[1] + " " + restaurant[2]
        text += "\n"

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, 'ID / Имя / Аддресс')


@bot.message_handler(commands='remove_restaurant')
def remove_restaurant(message):
    global respawn
    respawn = 'remove_restaurant'
    text = ''
    restaurants = get_all_restaurants()
    for restaurant in restaurants:
        text += str(restaurant[0]) + ")" + " " + restaurant[1] + " " + restaurant[2]
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Выберите ID")


@bot.message_handler(commands='add_food_type')
def add_food_type(message):
    global respawn
    respawn = 'add_food_type'
    bot.send_message(message.from_user.id, "Название")

@bot.message_handler(commands='add_food')
def add_food(message):
    global respawn
    respawn = "add_food"


    text = ""
    food_types = get_all_food_types()
    for f in food_types:
        text += str(f[0]) + ") " + f[1]
        text += '\n'
    bot.send_message(message.from_user.id, "Типы Блюда:")
    bot.send_message(message.from_user.id, text)

    text = ""
    restaurants = get_all_restaurants()
    for r in restaurants:
        text += str(r[0]) + ") " + r[1] + " " + r[2]
        text += '\n'
    bot.send_message(message.from_user.id, "Рестораны:")
    bot.send_message(message.from_user.id, text)

    bot.send_message(message.from_user.id, 'Имя / Цена / Описание / food_type_id / restaurant_id')

@bot.message_handler(commands='remove_food_type')
def removing_food_type(message):
    global respawn
    respawn = "remove_food_type"

    text = ''
    food_types = get_all_food_types()
    for ft in food_types:
        text += str(ft[0]) + ") " + ft[1]
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Введите ID")


@bot.message_handler(commands='remove_food')
def removing_food(message):
    global respawn
    respawn = "remove_food"

    text = ''
    foods = get_all_foods()
    for food in foods:
        text += str(food[0]) + ") " + food[1] + " " + str(food[2]) + " " + food[3] + " " + str(food[4]) + " " + str(food[5])
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Введите ID:")



@bot.message_handler(commands='edit_food_type')
def editing_food_type(message):
    global respawn
    respawn = 'edit_food_type'
    text = ''

    food_types = get_all_food_types()
    for ft in food_types:
        text += str(ft[0]) + ") " + ft[1]
        text += "\n"

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Введите ID/Имя")


@bot.message_handler(commands='edit_food')
def editing_food(message):
    global respawn
    respawn = "edit_food"
    text = ''

    foods = get_all_foods()
    for food in foods:
        text += str(food[0]) + ") " + food[1] + " " + str(food[2]) + " " + food[3] + " " + str(food[4]) + ' ' + str(food[5])
        text += '\n'

    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, 'Введите ID/Имя/Цену/Описание')


@bot.message_handler(commands='start')
def handle_user_menu(message):
    global respawn

    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Вы посетитель", reply_markup=hide_markup)

    text = ""
    text = text + "#########################\n"
    text = text + "Добро пожаловать в сервис заказа еды\n"
    text = text + "#########################\n"
    text = text + "Выберите опцию поиска: \n"
    text = text + "1 - Поиск по типу еды\n"
    text = text + "2 - Поиск по ресторану\n"

    bot.send_message(message.from_user.id, text)
    respawn = "user menu"


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global respawn

    if respawn == "user menu":
        if message.text.lower() == "1":
            food_types = get_all_food_types()
            text = "#####################\n"
            for food in food_types:
                text = text + str(food[0]) + ") " + food[1] + "\n"
            respawn = "choose_by_food_type"
            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, "Выберите тип блюда")
            log(message)

        elif message.text.lower() == "2":
            restaurants = get_all_restaurants()
            text = "#####################\n"
            for rest in restaurants:
                text = text + str(rest[0]) + ") " + rest[1] + " " + rest[2] + "\n"
            respawn = "choose_by_restaurant"
            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, "Выберите ресторан")

    elif respawn == "choose_by_food_type":
        respawn = "choose_food"
        id = message.text.lower()
        foods = get_foods_by_food_type(id)
        text = "#####################\n"
        for food in foods:
            text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + " " + food[3] + " " + str(food[4]) \
                   + "\n"

        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Выберите блюда")

    elif respawn == "choose_by_restaurant":
        respawn = "choose_food"
        id = message.text.lower()
        foods = get_foods_by_restaurant_id(id)
        text = "#####################\n"
        for food in foods:
            text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[3] + " - Тип блюда " + \
                   food[4] + "\n"

        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Выберите блюда")

    elif respawn == "choose_food":
        id = message.text.lower()
        food = get_food(id)

        text = "Вы заказали " + food[1] + " за " + str(food[2]) + " KZT\n"
        text = text + "Состав: [" + food[3] + "] \n"
        text = text + "К оплате: " + str(food[2]) + " KZT\n"
        text = text + "Спасибо за покупку\n"
        bot.send_message(message.chat.id, text)

    if respawn == "add_restaurant":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 2:
            insert_restaurant(values[0], values[1])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    elif respawn == "edit_restaurant":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 3:
            edit_restaurant(int(values[0]), values[1], values[2])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    elif respawn == "remove_restaurant":
        value = message.text

        if value.isdigit():
            delete_restaurant(value)
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    if respawn == "add_food_type":
        insert_food_type(message.text)
        bot.send_message(message.from_user.id, 'Успешно')

    if respawn == "add_food":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 5:
            insert_food(values[0], values[1], values[2], values[3], values[4])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    if respawn == "remove_food_type":
        values = message.text
        if values.isdigit():
            remove_food_type(values)
            bot.send_message(message.from_user.id, "Успешно")
        else:
            bot.send_message(message.from_user.id, "Введите в правильном формате")

    if respawn == "remove_food":
        values = message.text
        if values.isdigit():
            remove_food(values)
            bot.send_message(message.from_user.id, "Успешно")
        else:
            bot.send_message(message.from_user.id, "Введите в правильном формате")

    if respawn == "edit_food_type":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 2:
            edit_food_type(int(values[0]), values[1])
            bot.send_message(message.from_user.id, 'Успешно')
        else:
            bot.send_message(message.from_user.id, 'Введите в правильном формате')

    if respawn == "edit_food":
        values = message.text
        values = values.split('/')
        values = [v.strip() for v in values]

        if len(values) == 4:
            edit_food(int(values[0]), values[1], int(values[2]), values[3])
            bot.send_message(message.from_user.id, "Успешно")
        else:
            bot.send_message(message.from_user.id, "Введите в правильном формате")


bot.polling(none_stop=True, interval=0)