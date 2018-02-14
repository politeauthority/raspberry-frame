"""Option - MODEL

"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm.exc import NoResultFound

from app.models.base import Base


class Option(Base):

    __tablename__ = 'options'

    name = Column(String(50), nullable=False)
    value = Column(Text())

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            c = self.query.filter(Option.id == self.id).one()
            if c:
                self.__build_obj__(c)

    def __repr__(self):
        return '<Option %r, %r>' % (self.name, self.id)

    def __build_obj__(self, obj):
        """
        Sets the objects values

        :param obj: Current object
        :type obj: Option obj
        """
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.name = obj.name
        self.value = obj.instagram_id

    @staticmethod
    def get(option_name):
        """
        Gets an option value if it exists or nothing.

        :param option_name: Name of the option you're looking for.
        :type option_name: string
        :returns: The option value if it exists or nothign.
        :rtype: str
        """
        try:
            option = Option.query.filter(Option.name == option_name).one()
            return option.value
        except NoResultFound:
            return None
