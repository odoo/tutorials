from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_id = fields.One2many(
        "estate.property",
        "salesman_id",
        domain=[("state", "in", ("new", "offer_received"))],
    )
