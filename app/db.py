import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base 
from pathlib import Path 
from datetime import datetime 
from contextlib import contextmanager

#Читаем из env если нет то локальный путь (в тестах пусть лежит внутри app)
DB_PATH = Path(os.getenv("DB_PATH", Path(__file__).resolve().parent / "data" / "todo.db"))

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

#Задаем инфраструктуру
engine = create_engine(
   f"sqlite:///{DB_PATH}",
   echo = False, 
   future=True
)
Session = sessionmaker(bind = engine, autoflush=False, autocommit = False)
Base = declarative_base()

#создаем модель данных
class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)
    
#Инициализируем создание бд и таблиц 
def init_db():
    Base.metadata.create_all(bind = engine)


#создаем контекстный менеджер для сессии для корректного фиксирования изменений и закрытия сессии 
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise 
    finally:
        session.close()