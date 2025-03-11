from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"
    # property_ids=fields.One2many("estate.property","seller_id")
    property_ids = fields.One2many(
        "estate.property",  
        "seller_id",        # Inverse field (Many2one in estate.property) (Links the seller (user) to multiple properties)
        string="Properties",
        domain=[('state', '=', 'new')]  # Show only available properties
    )
