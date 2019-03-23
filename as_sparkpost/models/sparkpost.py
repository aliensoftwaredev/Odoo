# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev
from odoo import fields, models, api
import requests

class SparkPost(models.Model):
    _name = 'alsw.sparkpost'

    @api.multi
    def create_headers(self, content_type, authorization):
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        headers = {
            'User-Agent': user_agent,
            'Content-type': content_type,
            'Authorization': authorization
        }
        return headers

    @api.multi
    def send_email(self, receiver, sender, subject, content, content_type):
        access_token = self.env['alsw.sparkpost.config'].sudo().search([('active', '=', True)],
                                                                       order='id DESC',
                                                                       limit=1)
        if not access_token:
            return True, 'Your access token has been not found!'
        token = access_token.user_access_token
        url = 'https://api.sendgrid.com/v3/mail/send'
        header_content_type = 'application/json'
        authorization = 'Bearer ' + token
        headers = self.create_headers(header_content_type, authorization)
        #
        body = '{"personalizations": [{"to": [{"email": "' + receiver
        body += '"}], "subject": "' + subject
        body += '"}], "from": {"email": "' + sender
        body += '"}, "content": [{"type": "' + content_type
        body += '", "value": "' + content + '"}]}'

        session = requests.Session()
        r = session.post(url, data=body, headers=headers)
        error = str(r.content)
        if r.status_code >= 200 and r.status_code < 300:
            return True, error
        return False, error