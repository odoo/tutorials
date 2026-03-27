from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ['res.users']
    _name = 'res.users'

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesperson_id', domain=['|', ('state', '=', 'new'), ('state', '=', 'received')])
