# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'

    name = fields.Char('Estate Property', quired=True, translate='True')
    active = fields.Boolean('Active', default=True)
    price = fields.Float('Price', default=0)