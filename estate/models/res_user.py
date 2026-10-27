from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ["res.users"]
    _name = "res.users"
    _description = "Estate salespersons"

    property_ids = fields.One2many(
        "estate.property",
        inverse_name="user_id",
        string="Selling Properties",
        domain="['|',('state', '=', 'new'),('state', '=', 'offer_received')]",
    )
