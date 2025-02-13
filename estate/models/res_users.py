from odoo import api, fields, models

class RESUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesman_id",
        string="Properties",
        domain=[("state", "=", "sold")]
    )
