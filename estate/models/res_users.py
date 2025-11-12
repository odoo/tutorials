from odoo import fields, models

class users_inherited(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesman_id", 
        string="Properties",
        domain="[('state', 'in', ['New', 'Offer Received'])]"  
    )