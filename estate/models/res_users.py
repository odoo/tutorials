from odoo import fields, models


class resuserinherit(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "saler_id")
