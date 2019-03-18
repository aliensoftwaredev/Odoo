# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev

from odoo import api, models

class CreateEmployee(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals):
        res = super(CreateEmployee, self).create(vals)
        #
        if len(res.ids) > 0:
            for id in res.ids:
                load_user = self.env['res.users'].sudo().browse(id)
                vals_emp = {
                    'company_id': self.env.user.company_id.id or False,
                    'active': True,
                    'name': load_user.name,
                    'resource_calendar_id': 1,
                    'address_id': False,
                    'category_ids': [[6, False, []]],
                    'work_email': load_user.email,
                    'user_id': id,
                    'image': load_user.image
                }
                self.env['hr.employee'].create(vals_emp)
        #
        return res
