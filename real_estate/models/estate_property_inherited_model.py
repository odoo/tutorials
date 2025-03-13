from odoo import api,fields, models


class EstatePropertyInheritedMode(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesperson", domain=[("state", "not in", ["cancelled"])]
    )

