
from odoo import models
from datetime import datetime, time
from odoo.tools.misc import DEFAULT_SERVER_TIME_FORMAT

class Time(models.Field):
    type = 'time'
    column_type = ('time', 'time')
    column_cast_from = ('datetime',)

    def convert_to_cache(self, value, record, validate=True):
        if not value:
            return False
        if not isinstance(value, time):
            raise TypeError("%s (field %s) must be time." % (value, self))
        return value

    @staticmethod
    def to_string(value):
        return value.strftime(DEFAULT_SERVER_TIME_FORMAT) if value else False

    @staticmethod
    def to_time(value):
        return datetime.strptime(value, DEFAULT_SERVER_TIME_FORMAT).time() if value else False