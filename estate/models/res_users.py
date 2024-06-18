from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        domain=[("state", "!=", "canceled"), ("state", "!=", "sold")],
        string="Properties",
    )
