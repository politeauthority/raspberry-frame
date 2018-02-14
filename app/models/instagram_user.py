"""InstagramUser - MODEL

"""
from sqlalchemy import Column, String, Text, DateTime

from app.models.base import Base


class InstagramUser(Base):

    __tablename__ = 'user_instagram'

    name = Column(String(50), nullable=False)
    instagram_id = Column(Text(), nullable=False)
    last_checked = Column(DateTime)

    def __init__(self, _id=None):
        """
        Loads and sets an model object if an _id is passed in.

        :param _id: The id of the object to load.
        :type _id: int
        """
        if _id:
            self.id = _id
            self.__build_obj__()
        if _id:
            self.id = _id
            c = self.query.filter(InstagramUser.id == self.id).one()
            if c:
                self.__build_obj__(c)

    def __build_obj__(self, obj):
        """
        Loads and sets an model object if an _id is passed in.

        :param _id: The id of the object to load.
        :type _id: int
        """
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.name = obj.name
        self.instagram_id = obj.instagram_id
