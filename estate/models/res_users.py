from odoo import fields, models


class InheritedResUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Real Estate Properties', domain=[("status", "in", ["new", "offer_received"])])
