from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer received')]"
    )
