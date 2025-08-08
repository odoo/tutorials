from odoo import fields, models

class EstateUser(models.Model):
    '''Salesperson for estate'''
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string = "Properties")
