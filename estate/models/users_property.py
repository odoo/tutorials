from odoo import api, fields, models
from odoo.exceptions import UserError


class UserInherit(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        string="Properties",
        domain=["|", ("state", "!=", "cancelled"), ("state", "!=", "sold")],
    )
