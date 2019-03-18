# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev

from odoo import api, fields, models

class ActiveReactive(models.Model):
    _inherit = 'res.users'

    @api.multi
    def write(self, vals):
        res = super(ActiveReactive, self).write(vals)

        if 'active' in vals:
            if vals.get('active') == False:
                if len(self.ids) > 0:
                    for id in self.ids:
                        self.env['hr.employee'].sudo().search([('user_id', '=', id)]).write({'active': False})
            if vals.get('active') == True:
                if len(self.ids) > 0:
                    for id in self.ids:
                        query = "SELECT hr_employee.id FROM hr_employee WHERE hr_employee.resource_id in (SELECT resource_resource.id FROM resource_resource WHERE resource_resource.user_id = " + str(id) + ")"
                        self._cr.execute(query)
                        data = self._cr.dictfetchall()
                        if len(data) > 0:
                            for item in data:
                                self.env['hr.employee'].sudo().browse(item['id']).write({'active': True})

        return res