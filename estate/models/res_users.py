# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    # property_ids = fields.One2many('estate.property', 'user_id', string='Properties', domain=['|', ('state', '=', 'new'), ('state','=','offer_received')])
    property_ids = fields.One2many('estate.property', 'user_id', string='Properties') #removed domain for pdf report of sold properties
