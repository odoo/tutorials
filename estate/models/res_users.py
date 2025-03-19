from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',    
        'salesperson_id',        
        string="Properties",
        domain=[('state', 'in', ['new', 'offer_received'])]  
    )
