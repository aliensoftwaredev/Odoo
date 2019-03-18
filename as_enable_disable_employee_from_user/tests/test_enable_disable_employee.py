# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev

from odoo import tests
from odoo.tests import common

@tests.tagged('post_install', 'as_enable_disable_employee_from_user')
class TestPerm(common.TransactionCase):

    def default_user(self):
        company = self.env.ref('base.main_company').id
        vals = {
            'action_id': False,
            'lang': 'en_US',
            'active': True,
            'company_id': company,
            'notification_type': 'email',
            'company_ids': [[6, False, [company]]],
            'login': 'longth@gmail.com',
            'name': 'Trần Hoàng Long',
            'image': False,
            'alias_contact': False,
            'tz': 'Europe/Brussels',
            'email': 'longth@gmail.com',
            'signature': '<p><br></p>',
            'odoobot_state': 'not_initialized'
        }
        return vals

    def test_enable_disable_employee(self):
        user = self.env['res.users'].sudo().create(self.default_user())
        ids = user.employee_ids.ids
        self.assertEqual(len(ids), 1)
        self.assertEqual(user.employee_ids.name, 'Trần Hoàng Long')
        user.write({'active': False})
        self.assertEqual(user.employee_ids.active, False)
        user.write({'active': True})
        self.assertEqual(user.employee_ids.active, True)