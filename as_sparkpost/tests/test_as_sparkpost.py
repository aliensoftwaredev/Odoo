# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev

from odoo import tests
from odoo.tests import common
from odoo.addons.test_mail.tests.common import mail_new_test_user
import hashlib

@tests.tagged('post_install', 'as_sparkpost')
class Test(common.TransactionCase):

    def default_sparkpost(self):
        vals = {
            'name': 'Test',
            'username': 'raloja@myfavorite.info',
            'password': 'XeNnUMBRCR3G57MY',
            'active': True
        }
        return vals

    def test_get_access_token(self):
        config = self.env['alsw.sparkpost.config'].sudo().create(self.default_sparkpost())
        self.assertEqual(config.name, 'Test')
        #
        config.get_access_token()
        #
        raw = config.username + config.password
        duplicate = hashlib.md5(raw.encode("utf-8")).hexdigest()
        self.assertEqual(config.duplicate, duplicate)
        #
        smtp = config.create_smtp()
        self.assertEqual(smtp.name, 'Sparkpost SMTP')
        #
        smtp.unlink()
        config.unlink()