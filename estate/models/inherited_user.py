# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields

class InheritedUser(models.Model):
    _inherit="res.users"
    
    property_ids=fields.One2many("estate.property", "salesman_id", string="Property", domain=[('status', 'not in', ['sold', 'cancel'])])
