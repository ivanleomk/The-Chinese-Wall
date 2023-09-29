from fastapi_sqlalchemy import db

from db.models import Message


def insert_prompt_into_db(prompt: str, level: str, response_result: str):
    user_message = Message(level=level, prompt=prompt, response=response_result)
    db.session.add(user_message)
    db.session.commit()


def get_all_logs():
    return db.session.query(Message).limit(100).all()
