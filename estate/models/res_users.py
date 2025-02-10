from odoo import fields, models

class inheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        domain=[("status", "not in", ["sold", "cancelled"])],
    )

