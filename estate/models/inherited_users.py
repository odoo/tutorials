from odoo import models, fields


class InheritedUsers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(
        "estate.property",
        "sales_man",
        domain=[("state", "=", "new") or ("state", "=", "offer_received")],
        string="Properties",
    )

