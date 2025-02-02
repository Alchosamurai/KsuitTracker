import telebot
import src.config as config
from ..tracker.tracker import Tracker
from src.database.models.user import User
from src.database.models.task import Task
from src.core.utils import time_options, shedule 
from src.core.utils.shedule import start_scheduler
import re
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import logging  
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщений
    handlers=[
        logging.FileHandler("bot.log"),  # Запись логов в файл
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)
logger = logging.getLogger(__name__)  

bot = telebot.TeleBot(config.TG_BOT_TOKEN, parse_mode=None)
time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3])[: ]([0-5][0-9])$')



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    logger.info(f"User {message.from_user.username} (chat_id: {chat_id}) started the bot.")  
    User.create(message.from_user.username, chat_id)
    bot.reply_to(message, f"""
Привет, {message.from_user.username}!
*Инструкция*:\n
1) Просто при закрытии задачи отправь в чат время, которое указывается в заявке в ксуите, в формате ЧЧ:ММ или ЧЧ ММ\n
2) Бот сам рассчитает, сколько еще часов за сегодня осталось закрыть, чтобы не объебаться в конце месяца
""", reply_markup=create_keyboard(),parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "Статистика за сегодня 📊")
def send_today_stats(message):
    logger.info(f"User {message.from_user.username} (chat_id: {message.chat.id}) requested today's statistics.")  
    response = ""
    tasks = Task.today_user_stats(message.chat.id)
    total_time = timedelta(seconds=0)
    for task in tasks:
        response += f"{task.hour:02}:{task.min:02} в {task.datetime.hour:02}:{task.datetime.minute:02}\n"
        total_time += timedelta(hours=task.hour, minutes=task.min)
    response += f"*Общее время*: {time_options.timedelta_to_hhmm(total_time)}"
    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=create_keyboard())


@bot.message_handler(func=lambda message: time_pattern.match(message.text))
def handle_time(message):
    time = message.text.replace(' ', ':')
    logger.info(f"Received time input: {time} from user {message.from_user.username} (chat_id: {message.chat.id})")  
    actual_time = datetime.now()
    cur_time = Task.get_current_time_by_date(chat_id=message.chat.id, target_date=actual_time)
    cur_time = time_options.timedelta_to_hhmm(cur_time)
    tracker = Tracker(current_time=cur_time)
    cur_time = tracker.uppload_work_time(time)
    Task.create(message.chat.id, int(time.split(':')[0]), int(time.split(':')[1]))
    logger.info(f"Task created for user {message.from_user.username} (chat_id: {message.chat.id}) with time {time}.")  
    bot.reply_to(message, f"Осталось {cur_time} часов", reply_markup=create_keyboard())

def send_message_to_chat(chat_id: int, text: str):
    """
    Отправляет сообщение в указанный чат.
    :param chat_id: ID чата
    :param text: Текст сообщения
    """
    try:
        bot.send_message(chat_id, text)
        logger.info(f"Сообщение отправлено в чат {chat_id}.")
    except Exception as e:
        logger.info(f"Ошибка при отправке сообщения: {e}")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    user = User.get(message.chat.id)
    if user:
        name = user.name
        logger.info(f"Echo response sent to user {name} (chat_id: {message.chat.id}).")  
        bot.reply_to(message, str(f"Такой команды не обнаружено 🤡"))
    else:
        logger.warning(f"User not found for chat_id: {message.chat.id}.") 
        bot.reply_to(message, "Пользователь не найден.")


def create_keyboard():
    """
    Создает Reply-клавиатуру с одной кнопкой.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # Автоматическое изменение размера клавиатуры
    button = KeyboardButton("Статистика за сегодня 📊")
    #button2 = KeyboardButton("Статистика за весь месяц 📊📊📊")  # Текст на кнопке
    keyboard.add(button)
    #keyboard.add(button2)  # Добавляем кнопку в клавиатуру
    return keyboard

try:
    logger.info("Starting bot...")
    start_scheduler()
    bot.infinity_polling()
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)  