
from odoo import models, fields

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    property_ids = fields.One2many('estate_property', 'salesman_id', string='Estate Properties', domain=[('state', 'not in', ['canceled', 'sold'])])
