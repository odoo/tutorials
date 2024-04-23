from odoo import fields, models  # type: ignore


class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        domain="['|',('state', '=', 'new'),('state', '=', 'offer received')]",
    )
