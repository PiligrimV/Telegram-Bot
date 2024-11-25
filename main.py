import telebot, os
from dotenv import load_dotenv
from telebot import types
from PIL import Image

# Загрузка переменных окружения из файла .env
load_dotenv()

# Определение алфавита
alphabet = os.getenv('ALPHABET')

#########################################
#########################################

user_states = {}

def set_user_state(chat_id, state):
    user_states[chat_id] = state

def get_user_state(chat_id):
    return user_states.get(chat_id, "normal")

#########################################
#########################################

# Функция шифровки
def encode(text, output_image_path):
    # Определяем размер изображения
    image_size_x = len(alphabet)
    image_size_y = len(text) + 20
    
    # Создаем новое изображение для кодирования текста
    encoded_image = Image.new("RGB", (image_size_x, image_size_y), color="white")
    
    # Кодируем текст в изображение по его координатам
    for i, char in enumerate(text):
        x = int(alphabet.find(char))
        y = i
        encoded_image.putpixel((x, y), (0, 0, 0))  # Задаем пиксель
    
    # Сохраняем изображение с закодированным текстом
    encoded_image.save(output_image_path, quality=100)

# Функция расштфровки
def decode(input_image_path):
    # Открываем изображение с закодированным текстом
    encoded_image = Image.open(input_image_path)
    width, height = encoded_image.size
    decoded_text = ""
    
    # Декодируем текст из черных пикселей изображения
    for y in range(height):
        for x in range(width):
            pixel = encoded_image.getpixel((x, y))
            if pixel == (0, 0, 0):  # Проверяем, является ли пиксель черным
                char_index = x  # Используем координату x для определения символа
                decoded_text += alphabet[char_index % len(alphabet)]
    
    return decoded_text

#########################################
#########################################

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🛠️Зашифровать')
    item2 = types.KeyboardButton('💻Расшифровать')
    item3 = types.KeyboardButton('⚠️Информация')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Привет, дорогой друг', reply_markup = markup)

    set_user_state(message.chat.id, "normal")

@bot.message_handler(content_types=['text', 'document'])
def bot_commands(message):
    # Проверяем состояние пользователя
    user_state = get_user_state(message.chat.id)

    if user_state == "waiting_for_input":
        if message.content_type == 'text':
            # Пользователь вводит текст для шифрования
            text_to_encode = message.text
            output_image_path = f"{message.chat.id}_encoded_image.jpg"  # Путь для сохранения изображения в формате JPG
            encode(text_to_encode, output_image_path)
            
            # Отправляем изображение пользователю
            with open(output_image_path, "rb") as image_file:
                bot.send_document(message.chat.id, image_file)

            # Удаляем временный файл с изображением
            os.remove(output_image_path)

            # Возвращаемся к обычному состоянию
            set_user_state(message.chat.id, "normal")
        
        elif message.content_type == 'document':
            # Получаем информацию о картинке
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image_path = f"{message.chat.id}_decode_image.jpg"  # Путь для сохранения изображения в формате JPG

            # Сохраняем картинку
            with open(image_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Декодируем текст из изображения
            decoded_text = decode(image_path)

            # Отправляем декодированный текст
            bot.send_message(message.chat.id, f"Декодированный текст: {decoded_text}")

            # Удаляем временный файл с изображением
            os.remove(image_path)

            # Возвращаемся к обычному состоянию
            set_user_state(message.chat.id, "normal")

    if message.text == 'SOONAMI':
        bot.send_message.chat.id, 'Бот создан SOONAMI STUDIOS'
    elif message.text == '⚠️Информация':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🤖О Боте')
        item2 = types.KeyboardButton('👨🏻‍💻Тех.Поддержка')
        back = types.KeyboardButton('⬅️Назад')
        markup.add(item1, item2, back)
    
        bot.send_message(message.chat.id, '⚠️Информация', reply_markup = markup)

    elif message.text == '🤖О Боте':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back = types.KeyboardButton('⬅️Назад')
        markup.add(back)
    
        bot.send_message(message.chat.id, 'Versions 1.0.0, Бот создан SOONAMI STUDIOS vk.com/soonami.group', reply_markup = markup)
    
    elif message.text == '👨🏻‍💻Тех.Поддержка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back = types.KeyboardButton('⬅️Назад')
        markup.add(back)
    
        bot.send_message(message.chat.id, '✏️VK: vk.com/soonami.group', reply_markup = markup)
    
    elif message.text == '💻Расшифровать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🛠️Зашифровать')
        item2 = types.KeyboardButton('💻Расшифровать')
        item3 = types.KeyboardButton('⚠️Информация')
        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, 'Отправьте картинку без сжатия', reply_markup = markup)

        set_user_state(message.chat.id, "waiting_for_input")
        
    elif message.text == '🛠️Зашифровать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🛠️Зашифровать')
        item2 = types.KeyboardButton('💻Расшифровать')
        item3 = types.KeyboardButton('⚠️Информация')
        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, 'Введите текст', reply_markup = markup)

        set_user_state(message.chat.id, "waiting_for_input")
                
    elif message.text == '⬅️Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🛠️Зашифровать')
        item2 = types.KeyboardButton('💻Расшифровать')
        item3 = types.KeyboardButton('⚠️Информация')
        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, '⬅️Назад', reply_markup = markup)
            
bot.polling()
