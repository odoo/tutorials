from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="user_id",
        string='Available Properties',
        domain=["|", ("state", "=", "new"), ("state", "=", "offer_received")],
    )
