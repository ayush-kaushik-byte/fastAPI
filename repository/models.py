from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    creation_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('Users.id'))
    creator = relationship('User', back_populates='tasks')

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    tasks = relationship('Task', back_populates='creator')
    