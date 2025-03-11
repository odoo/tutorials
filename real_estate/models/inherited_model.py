from odoo import fields, models


class InheritedMode(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesperson", domain=[("state", "not in", ["cancelled"])]
    )
