from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "seller",
        string="Properties",
        domain=[('state', '!=', 'cancelled')]
    )
