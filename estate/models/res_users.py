from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        domain=[("state", "=", "new") or ("state", "=", "offer_received")],
        string="Properties",
    )

