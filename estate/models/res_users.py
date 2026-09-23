from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        string="Real Estate Properties",
        domain=[('date_availability', '>', fields.Date.today())],
    )
