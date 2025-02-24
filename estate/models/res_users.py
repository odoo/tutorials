# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class InheritedUser(models.Model):
    _inherit = 'res.users'
    
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesman_id', string="Property", domain=[('state', 'not in', ['sold', 'cancel'])])
