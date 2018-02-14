"""Media - MODEL

"""
from sqlalchemy import Column, String, Text, DateTime, Integer, UniqueConstraint

from app.models.base import Base


class Media(Base):

    __tablename__ = 'media'

    url = Column(String(500), nullable=False)
    file = Column(String(200))
    description = Column(Text())
    content_type = Column(String(50))
    domain = Column(String(50))
    author = Column(String(200))
    media_created = Column(DateTime)
    file_size = Column(Integer)
    score = Column(Integer)
    downloaded = Column(Integer)

    __table_args__ = (
        UniqueConstraint('url', 'file', name='uix_1'),
    )

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            c = self.query.filter(Media.id == self.id).one()
            if c:
                self.__build_obj__(c)

    def __build_obj__(self, obj):
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.url = obj.url
        self.file = obj.file
        self.description = obj.description
        self.content_type = obj.content_type
        self.domain = obj.domain
        self.author = obj.author
        self.media_created = obj.media_created
        self.l_url = "content/%s.%s" % (self.file, self.content_type)
