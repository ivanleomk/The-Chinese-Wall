# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('messages_id_seq'::regclass)"),
    )
    timestamp = Column(DateTime, nullable=False, server_default=text("now()"))
    level = Column(String(255), nullable=False)
    prompt = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)
