from odoo import fields, models


class EstateUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "seller_id")
