from odoo import models, fields

class inheritedUser(models.Model):
    _inherit = 'res.users'
    
    property_ids=fields.One2many('estate.property', 'salesman_id')