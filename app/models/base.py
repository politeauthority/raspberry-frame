"""Base - Model

"""
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.exc import IntegrityError

import app
from app import db


class Base(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return '<%s %r, %r>' % (self.__class__.__name__, self.id)

    def save(self):
        if not self.id:
            try:
                db.session.add(self)
            except IntegrityError, e:
                app.log.warning(e)
        db.session.commit()

# End File: raspberry-frame/app/models/base.py
