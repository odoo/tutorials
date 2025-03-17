from odoo import fields , models

class EstateResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string= "Properties",
        domain="['|',('state', '=', 'new'), ('state', '=', 'offer_received')]",
    )
