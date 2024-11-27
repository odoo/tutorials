from odoo import fields, models

class users_inherited(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property", 
        inverse_name="salesman", 
        string="Properties",
        domain="[('state', 'in', ['New', 'Offer Received'])]"  
    )