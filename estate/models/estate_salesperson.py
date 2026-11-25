from odoo import fields, models


class Salesperson(models.Model):
    _inherit = ["res.users"]
    _name = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        name="Properties",
        domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]
        )
