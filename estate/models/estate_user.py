from odoo import models, fields


class EstateUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        "estate",
        "seller_id",
        string="My Properties",
        domain=[("state", "not in", ["sold", "cancelled"]), ("active", "=", True)],
    )
