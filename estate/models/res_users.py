from odoo import fields, models

class ResUsers(models.Model):
    pass
    _inherit = ["res.users"]

    property_ids = fields.One2many('estate_property', 'salesperson', domain=[('state', 'in', ('new', 'offer received'))])
