# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev

from odoo import tests
from odoo.tests import common
from odoo.addons.test_mail.tests.common import mail_new_test_user
from odoo.exceptions import AccessError
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

    def test_access_rights_sa(self):
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

    def test_access_rights_as(self):
        # Administration/Settings
        user = mail_new_test_user(self.env, login='adam', groups='base.group_system')
        config = self.env['alsw.sparkpost.config'].sudo(user.id).create(self.default_sparkpost())
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

    def test_access_rights_user(self):
        # Administration/Settings
        user = mail_new_test_user(self.env, login='adam', groups='base.group_user')
        with self.assertRaises(AccessError):
            self.env['alsw.sparkpost.config'].sudo(user.id).create(self.default_sparkpost())

    def test_send_email(self):
        config = self.env['alsw.sparkpost.config'].sudo().create(self.default_sparkpost())
        self.assertEqual(config.name, 'Test')
        #
        config.get_access_token()
        #
        to_email = 'leli@postemail.net'
        from_name = 'Test Send Email'
        from_email = 'raloja@myfavorite.info'
        subject = 'This is a test email'
        content = 'Thanks for reading my email!'
        check, result = self.env['alsw.sparkpost'].send_email(to_email, from_name, from_email, subject, content)
        self.assertTrue(check)