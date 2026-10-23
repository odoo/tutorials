from odoo import fields, models


class ResUSers(models.Model):
    _inherit = "res.users"

    property_id = fields.One2many(
        "estate.property",
        "sales_man_id",
        domain=[("state", "in", ("new", "offer_received"))],
    )
