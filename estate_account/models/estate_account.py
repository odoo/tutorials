# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name="estate.account"
    _description="invoicing for estate module"
    
    name = fields.Char('Name', required=True)