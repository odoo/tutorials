from odoo import fields, models


class ResUsers(models.Model):
    # _name = "res.inherited.model"
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson",
        domain=[("state", "in", ["new", "offer_received"])],
    )
