import threading

from sqlalchemy import Column, String

from TitanXManager.modules.sql import BASE, SESSION


class TitanXSupport(BASE):
    __tablename__ = "TitanXSupport"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


TitanXSupport.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_titan(chat_id):
    try:
        chat = SESSION.query(TitanXSupport).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_titan(chat_id):
    with INSERTION_LOCK:
        titanxsupport = SESSION.query(TitanXSupport).get(str(chat_id))
        if not TitanXSupport:
            titanxsupport = TitanXSupport(str(chat_id))
        SESSION.add(titanxsupport)
        SESSION.commit()


def rem_titan(chat_id):
    with INSERTION_LOCK:
        titanxsupport = SESSION.query(TitanXSupport).get(str(chat_id))
        if titanxsupport:
            SESSION.delete(titanxsupport)
        SESSION.commit()
