from odoo import fields, models


class EstateUsersModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        domain=["|", ("state", "=", "new"), ("state", "=", "offer_received")],
    )
