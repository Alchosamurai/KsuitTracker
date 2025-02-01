from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from ..engine import Base, engine

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    chat_id = Column(Integer, unique=True)

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
            user = cls(name=name, chat_id=chat_id)
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
    def create_table(cls):
        Base.metadata.create_all(engine)
        print("Таблицы успешно созданы!")

