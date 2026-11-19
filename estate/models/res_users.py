from odoo import fields, models

class InheritedUsers(models.Model):
    _inherit = "res.users"

    estate_property_ids = fields.One2many('estate.property', 'salesman_id', string='Estate Properties', domain="[('state', 'not in', ('sold', 'cancelled'))]")
