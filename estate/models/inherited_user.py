from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", inverse_name="salesperson")
