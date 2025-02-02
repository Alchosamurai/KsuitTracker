from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from ..engine import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    chat_id = Column(Integer, unique=True)
    daily_target_hour = Column(Integer, default=8)
    daily_target_min = Column(Integer, default=0)
    monthly_target_hour = Column(Integer, default=160)

    @classmethod
    def create(cls, name: str, chat_id: int):
        """
        Создает нового пользователя и сохраняет его в базу данных.
        :param name: Имя пользователя
        :param chat_id: Уникальный идентификатор чата
        :return: Созданный объект пользователя
        """
        with Session(engine) as session:
            # Проверяем, существует ли пользователь с таким chat_id
            exists = session.query(cls).filter(cls.chat_id == chat_id).first() is not None
            if exists:
                return session.query(cls).filter(cls.chat_id == chat_id).first()
            
            # Создаем нового пользователя
            user = cls(name=name, chat_id=chat_id, daily_target_hour=8, daily_target_min=0, monthly_target_hour=160)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    @classmethod
    def get(cls, chat_id: int):
        """
        Получает пользователя из базы данных по chat_id.
        :param chat_id: Уникальный идентификатор чата
        :return: Объект пользователя или None, если пользователь не найден
        """
        with Session(engine) as session:
            return session.query(cls).filter(cls.chat_id == chat_id).first()
    
    @classmethod
    def get_all(cls):
        """
        Получает всех пользователей из базы данных.
        :return: Список объектов пользователей
        """
        with Session(engine) as session:
            return session.query(cls).all()
    
    @classmethod
    def update(cls, chat_id: int, **kwargs):
        """
        Обновляет поля пользователя по chat_id.
        :param chat_id: Уникальный идентификатор чата
        :param kwargs: Поля и их новые значения (например, name="Новое имя")
        :return: Обновленный объект пользователя или None, если пользователь не найден
        """
        with Session(engine) as session:
            # Находим пользователя по chat_id
            user = session.query(cls).filter(cls.chat_id == chat_id).first()
            if not user:
                return None  # Пользователь не найден
            
            # Обновляем поля
            for key, value in kwargs.items():
                if hasattr(user, key):  # Проверяем, существует ли поле
                    setattr(user, key, value)
            
            session.commit()  # Сохраняем изменения
            session.refresh(user)  # Обновляем объект
            return user

    @classmethod
    def create_table(cls):
        Base.metadata.create_all(engine)
        print("Таблицы успешно созданы!")

