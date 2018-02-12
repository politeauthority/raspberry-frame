"""Media - MODELS

"""
from sqlalchemy import Column, String, Text, DateTime, Integer

from app.models.base import Base


class Media(Base):

    __tablename__ = 'media'

    url = Column(Text(), nullable=False)
    file = Column(Text(), nullable=False)
    content_type = Column(String(50))
    domain = Column(String(50))
    author = Column(String(200))
    media_created = Column(DateTime)
    file_size = Column(Integer, primary_key=True)

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            c = self.query.filter(Media.id == self.id).one()
            if c:
                self.__build_obj__(c)

    def __repr__(self):
        return '<Media %r, %r>' % (self.id, self.url)

    def __build_obj__(self, obj):
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.url = obj.url
        self.file = obj.file
        self.domain = obj.domain
        self.author = obj.author
        self.media_created = obj.media_created
