from odoo import fields, models


class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate_property",
        "salesman_id",
        string="Offers",
        domain="['|',('state', '=', 'offer received'),('state', '=', 'offer accepted')]",
    )
