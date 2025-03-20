from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'
    
    property_ids = fields.One2many('estate.property', 'sales_person', string='Properties')
