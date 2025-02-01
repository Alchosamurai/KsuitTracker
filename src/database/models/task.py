from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from ..engine import Base, engine
from datetime import datetime, timedelta

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    hour = Column(Integer)
    min = Column(Integer)
    datetime = Column(DateTime)

    @classmethod
    def create(cls, chat_id: int, hour: int, min: int):
        """
        Создает новую задачу и сохраняет ее в базу данных.
        :param chat_id: Идентификатор чата
        :param hour: Час
        :param min: Минута
        :return: Созданный объект задачи
        """
        with Session(engine) as session:
            # Создаем объект задачи
            task = cls(chat_id=chat_id, hour=hour, min=min, datetime=datetime.now())
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
    @classmethod
    def get_by_date(cls, target_date):
        """
        Получает все задачи, созданные в указанную дату.
        :param target_date: Дата для фильтрации (тип date)
        :return: Список задач
        """
        with Session(engine) as session:
            # Преобразуем дату в начало и конец дня
            start_of_day = datetime(target_date.year, target_date.month, target_date.day)
            end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
            
            # Ищем задачи, созданные в указанный день
            tasks = session.query(cls).filter(
                cls.datetime >= start_of_day,
                cls.datetime <= end_of_day
            ).all()
            return tasks
        
    @classmethod
    def get_current_time_by_date(cls, chat_id, target_date):
        """
        Получает текущее время по дате.
        :param target_date: Дата для фильтрации (тип date)
        :return: время itmedelta сколько уже есть в базе по дате 
        """
        with Session(engine) as session:
            # Преобразуем дату в начало и конец дня
            start_of_day = datetime(target_date.year, target_date.month, target_date.day)
            end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
            
            # Ищем задачи, созданные в указанный день
            tasks = session.query(cls).filter(
                cls.chat_id == chat_id,
                cls.datetime >= start_of_day,
                cls.datetime <= end_of_day
            ).all()
            time = timedelta(hours=0, minutes=0)
            for task in tasks:
                time += timedelta(hours=task.hour, minutes=task.min)
            return time
    @classmethod
    def today_user_stats(cls, chat_id):
        with Session(engine) as session:
            # Преобразуем дату в начало и конец дня
            target_date = datetime.now()
            start_of_day = datetime(target_date.year, target_date.month, target_date.day)
            end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
            
            # Ищем задачи, созданные в указанный день
            tasks = session.query(cls).filter(
                cls.chat_id == chat_id,
                cls.datetime >= start_of_day,
                cls.datetime <= end_of_day
            ).all()
            return tasks
    @classmethod
    def create_table(cls):
        Base.metadata.create_all(engine)
        print("Таблицы успешно созданы!")
