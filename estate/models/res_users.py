from odoo import fields, models


class PropertyTag(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many('estate.property', 'salesperson', string='Properties')