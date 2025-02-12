from odoo import models, fields

class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "seller_id", string="property"
    )
