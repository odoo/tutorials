from odoo import models, fields


class ResUsersEstate(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(
        "estate.property",
        "seller_id",
        "Properties",
        domain=[("status", "in", ["new", "offer_received"])],
    )
