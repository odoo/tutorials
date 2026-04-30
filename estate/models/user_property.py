from odoo import fields, models


class UserProperties(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "seller_id", domain=[('state', '=', 'offer_received')],
    )
