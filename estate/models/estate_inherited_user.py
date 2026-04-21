from odoo import fields, models


class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Related Property",
        domain=["|", ("state", "=", "new"), ("state", "=", "received")],
    )
