from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesman_id', string='Real Estate Properties', domain=[("state", "in", ["new", "offer_received"])])
    