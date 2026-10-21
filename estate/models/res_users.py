# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    property_ids = fields.One2many('estate_property', 'salesman_id', string='Estate Properties', domain=[('state', 'not in', ['canceled', 'sold'])])

