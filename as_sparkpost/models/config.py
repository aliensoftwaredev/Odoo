# -*- coding: utf-8 -*-
# Part of Alien Software - aliensoftware.dev
from odoo import fields, models, api, _
from odoo.exceptions import Warning, UserError
import requests
import json
import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Config(models.Model):
    _name = 'alsw.sparkpost.config'
    _description = 'ALSW - Sparkpost'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    duplicate = fields.Char(string='Duplicate', store=True, readonly=True)
    web_access_token = fields.Char(string='Web Access Token')
    user_access_token = fields.Char(string='User Access Token')
    active = fields.Boolean(string='Active', default=True)
    expiry_date = fields.Datetime(string='Expiry Date', store=True, readonly=True)

    @api.constrains('username', 'password')
    def _cons_duplicate(self):
        raw = self.username + self.password
        duplicate = hashlib.md5(raw.encode("utf-8")).hexdigest()
        check = self.env['alsw.sparkpost.config'].sudo().search([('duplicate', '=', duplicate)])
        if check:
            raise Warning(_('Do not allow account duplication!'))
        else:
            self.duplicate = duplicate

    @api.multi
    def create_expiry_date(self, exp):
        exp = exp - 300
        exp_date = datetime.now() + relativedelta(seconds=exp)
        self.expiry_date = exp_date

    @api.multi
    def get_list_api_by_label(self, label):
        url = 'https://api.sparkpost.com/api/v1/api-keys'
        content_type = 'application/json;charset=utf-8'
        authorization = self.web_access_token
        if not self.web_access_token:
            return []
        headers = self.env['alsw.sparkpost'].sudo().create_headers(content_type, authorization)
        #
        result = []
        session = requests.Session()
        r = session.get(url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            if 'results' in data:
                for item in data['results']:
                    if item['label'] == label:
                        result.append(item['id'])
        return result

    @api.multi
    def remove_api_by_label(self, label):
        list_api = self.get_list_api_by_label(label)
        if len(list_api) > 0:
            for item in list_api:
                url = 'https://api.sparkpost.com/api/v1/api-keys/' + item
                content_type = 'application/json;charset=utf-8'
                authorization = self.web_access_token
                headers = self.env['alsw.sparkpost'].sudo().create_headers(content_type, authorization)
                #
                session = requests.Session()
                r = session.delete(url, headers=headers)
                if r.status_code == 200:
                    if 'Successfully' in r.text:
                        pass

    @api.multi
    def get_access_token_web(self):
        url = 'https://api.sparkpost.com/api/v1/authenticate'
        content_type = 'application/x-www-form-urlencoded'
        authorization = 'Basic bXN5c1dlYlVJOmZhODZkNzJlLTYyODctNDUxMy1hZTdmLWVjOGM4ZmEwZDc2Ng=='
        headers = self.env['alsw.sparkpost'].sudo().create_headers(content_type, authorization)
        #
        body = 'grant_type=password&username=' + self.username + '&password=' + self.password + '&rememberMe=false'
        session = requests.Session()
        r = session.post(url, data=body, headers=headers)
        data = json.loads(r.text)
        if r.status_code == 200:
            self.write({'web_access_token': data['access_token']})
            self.create_expiry_date(data['expires_in'])
        else:
            if 'error' in data:
                raise Warning(_(data['error']))
            else:
                raise Warning(_('You should check your username or password!'))

    @api.multi
    def create_access_token_user(self):
        url = 'https://api.sparkpost.com/api/v1/api-keys'
        content_type = 'application/json;charset=utf-8'
        authorization = self.web_access_token
        headers = self.env['alsw.sparkpost'].sudo().create_headers(content_type, authorization)
        #
        name = 'Odoo - Sparkpost'
        body = '{"grants":["metrics/view","message_events/view","webhooks/view","webhooks/modify","templates/view","templates/modify","templates/preview","transmissions/view","transmissions/modify","smtp/inject","recipient_lists/manage","tracking_domains/view","tracking_domains/manage","sending_domains/manage","inbound_domains/manage","suppression_lists/manage","relay_webhooks/view","relay_webhooks/modify","account/view","account/read-write","subaccount/manage","subaccount/view","ip_pools/manage","ip_pools/view","ab-testing/manage","alerts/manage"],"label":"' + name + '","valid_ips":[]}'
        session = requests.Session()
        r = session.post(url, data=body, headers=headers)
        data = json.loads(r.text)
        if r.status_code == 200:
            if 'results' in data and 'key' in data['results']:
                self.write({'user_access_token': data['results']['key']})
        else:
            if 'error' in data:
                raise Warning(_(data['error']))
            else:
                raise Warning(_('You should check your api!'))

    @api.multi
    def get_access_token(self):
        self.remove_api_by_label('Odoo - Sparkpost')
        self.get_access_token_web()
        self.create_access_token_user()

    @api.multi
    def active_account(self):
        body = """
        {
            "options": {
              "sandbox": true
            },
            "content": {
              "from": "sandbox@sparkpostbox.com",
              "subject": "Thundercats are GO!!!",
              "text": "Sword of Omens, give me sight BEYOND sight"
            },
            "recipients": [{ "address": "wehelp@microsoft.com" }]
        }
        """
        url = 'https://api.sparkpost.com/api/v1/transmissions'
        content_type = 'application/json;charset=utf-8'
        authorization = self.user_access_token
        headers = self.env['alsw.sparkpost'].sudo().create_headers(content_type, authorization)
        #
        session = requests.Session()
        r = session.post(url, data=body, headers=headers)
        data = json.loads(r.text)
        if r.status_code == 200:
            raise Warning(_('Your account may be successfully activated!'))
        else:
            raise Warning(_('Please check your access token!'))

    @api.multi
    def create_smtp(self):
        result = False
        if self.user_access_token:
            vals = {
                'name': 'Sparkpost SMTP',
                'smtp_host': 'smtp.sparkpostmail.com',
                'smtp_port': 587,
                'smtp_user': 'SMTP_Injection',
                'smtp_pass': self.user_access_token,
                'smtp_encryption': 'starttls',
                'sequence': 15,
                'active': True
            }
            check = self.env['ir.mail_server'].sudo().search([('name', '=', 'Sparkpost SMTP')])
            if check:
                check.unlink()
            result = self.env['ir.mail_server'].create(vals)
            return result
        return result