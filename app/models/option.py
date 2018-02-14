"""Option - MODEL
Quick thrown together model to get and set options for an app.

"""
from sqlalchemy import Column, String, Text, UniqueConstraint
from sqlalchemy.orm.exc import NoResultFound

from app.models.base import Base


class Option(Base):

    __tablename__ = 'options'

    name = Column(String(50), nullable=False)
    value = Column(Text())

    __table_args__ = (
        UniqueConstraint('name', name='uix_1'),
    )

    def __init__(self, _id=None):
        """
        Loads and sets an model object if an _id is passed in.

        :param _id: The id of the object to load.
        :type _id: int
        """
        if _id:
            self.id = _id
            c = self.query.filter(Option.id == self.id).one()
            if c:
                self.__build_obj__(c)

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
        :returns: The Option ob if it exists or nothign.
        :rtype: Option obj
        """
        try:
            option = Option.query.filter(Option.name == option_name).one()
            return option
        except NoResultFound:
            return None

    @staticmethod
    def set_defaults(options):
        """
        Sets default Options for an application easily.
        If the option passed in is a list, option default values will be Null, if options is a dict the keys and values
        is used to set the values.

        :param options: The option pairs to set.
        :type options: dict or list
        """
        option_dict = {}
        if isinstance(options, dict):
            option_dict = options
        else:
            for opt in options:
                option_dict[opt] = None
        for opt_name, opt_default_value in option_dict.iteritems():
            Option.check_option_and_set_default(opt_name, opt_default_value)

    @staticmethod
    def check_option_and_set_default(option_name, option_default_value):
        """
        Checks if an option exists and writes the default value if it does not.

        :param option_name: The key of the option to be set.
        :type option_name: str
        :param option_default_value: The default for the option.
        :type option_default_value: str
        """
        if not Option.get(option_name):
            o = Option()
            o.name = option_name
            o.value = option_default_value
            o.save()

# End File: raspberry-frame/app/models/option.py
