from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        domain=[("state", "=", "new")],
        string="Properties",
        help="The salesperson handling these properties",
    )
