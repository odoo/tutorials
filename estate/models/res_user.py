from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate_property",
        "salesperson",
        domain=["|", ("status", "=", "new"), ("status", "=", "offer_received")],
        string="Properties",
    )
