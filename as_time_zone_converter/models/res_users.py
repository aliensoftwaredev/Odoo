# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, api
import pytz

class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def alsw_convert_utc_to_local(self, utc_dt):
        time_zone = self._context.get('tz') or self.env.user.tz or 'UTC'
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone))
        return pytz.timezone(time_zone).normalize(local_dt)

    @api.model
    def alsw_convert_utc_to_date_local(self, utc_dt):
        return self.alsw_convert_utc_to_local(utc_dt).strftime(DEFAULT_SERVER_DATE_FORMAT)

    @api.model
    def alsw_convert_utc_to_datetime_local(self, utc_dt):
        return self.alsw_convert_utc_to_local(utc_dt).strftime(DEFAULT_SERVER_DATETIME_FORMAT)