from odoo import fields, models

class InheritModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'user_id', string='Properties')
