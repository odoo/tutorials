from odoo import fields, models

class InheritedUserModel(models.Model) : 
    _inherit = "res.users"
    property_ids = fields.One2many('public.property','salesperson' , domain = [('active','=',True)])
