import threading
import schedule
import time
from datetime import datetime, timedelta
from src.database.models.user import User
from src.database.models.task import Task
from sqlalchemy.orm import Session


def job():
    """Функция, которая будет вызываться в 16:00."""
    from ..tg_bot.tg_bot import send_message_to_chat as send
    users = User.get_all()
    work_day = timedelta(hours=8)
    for user in users:
        task = Task.get_current_time_by_date(user.chat_id, datetime.now())
        message = build_message(user, work_day - task)
        send(user.chat_id, message)
    print(f"Задача выполнена в {datetime.now().strftime('%H:%M:%S')}")
def resurs_reminder():
    """Функция, которая будет вызываться в 08:15 для напоминания протыкать ресурс."""
    from ..tg_bot.tg_bot import send_message_to_chat as send
    users = User.get_all()
    for user in users:
        send(user.chat_id, "А ты в *Ресурсе?!*")
    print(f"Задача выполнена в {datetime.now().strftime('%H:%M:%S')}")

    # Здесь можно добавить логику, например, отправить сообщение в телеграм
    # bot.send_message(chat_id, "Напоминание: 16:00!")
def build_message(user, time):
    if time > timedelta(hours=0, minutes=0):
        return f"""Похоже, уже 16:00, но нужное время на выполнение задач еще не закрыто...
        {user.name}, осталось закрыть на {time} часов"""
    else:
        return f"""Похоже, уже 16:00, и все задачи уже закрыты.
        Хорошая работа, {user.name}!"""
def run_scheduler():
    """Запуск планировщика в отдельном потоке."""
    schedule.every().day.at("16:00").do(job)
    schedule.every().day.at("08:15").do(resurs_reminder)
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_scheduler():
    """Запуск планировщика в отдельном потоке."""
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # Поток завершится, когда основной поток завершится
    scheduler_thread.start()



