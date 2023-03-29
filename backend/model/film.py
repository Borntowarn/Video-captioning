from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///films.db')

# Создаем экземпляр базового класса declarative_base
Base = declarative_base()


class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    hash = Column(String, unique=True)
    input_filename = Column(String)
    output_video_filename = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print('Создание генератора сессии')


def clear():
    session = Session()
    try:
        # Удалить все записи с id > 3
        session.commit()
    finally:
        session.close()


