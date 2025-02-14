# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'saleperson_id', string='Properties', domain=[('state', 'in', ('new', 'offer_received'))])
