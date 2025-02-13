from odoo import fields,models 

class InheritedUsers(models.Model):
    _inherit='res.users'
    
    property_ids = fields.One2many('estate.property',inverse_name='seller_id',domain="([ ('status', 'in', ('new','offer_received'))])")
    