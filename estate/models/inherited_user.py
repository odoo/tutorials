from odoo import fields, models  # type: ignore


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate_property",
        "user_id",
        domain="['|',('state', '=', 'new'),('state', '=', 'offer received')]",
    )
