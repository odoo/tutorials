from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        domain=[
            ("date_availability", ">=", fields.Date.today()),
            ("state", "in", ["new", "offer_received", "offer_accepted"]),
        ],
    )
