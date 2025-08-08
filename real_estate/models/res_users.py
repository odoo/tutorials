from odoo import models, fields

class InheritResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", 
        "salesperson_id",  
        string="Available Properties",
        domain=[('state' , 'in' ,['new'])]
    )
