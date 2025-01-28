from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate_property', 'users_id', string="Properties", domain=[('state', '=', 'available')])