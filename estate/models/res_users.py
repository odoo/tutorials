from odoo import models, fields


class ResUsers(models.Model):
    # Private attributes
    _inherit = "res.users"

    # Field declarations
    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        domain=[("state", "not in", ["sold", "cancelled"])]
    )
