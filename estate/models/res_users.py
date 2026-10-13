from odoo import fields, models


class InheritedResUsers(models.Model):
    _inherit = "res.users"
    _description = "Inherited Res Users"

    property_ids = fields.One2many(
        "estate.property",
        "sales_person",
        string="User Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
