# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Ward(models.Model):
    _description = 'Ward'
    _name = 'res.country.ward'
    _order = 'code'

    district_id = fields.Many2one('res.country.district', string='District', required=True)
    active = fields.Boolean(default=True)
    name = fields.Char(string='Ward Name', required=True)
    code = fields.Char(string='Ward Code', required=True)