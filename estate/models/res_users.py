from odoo import fields, models


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    property_ids = fields.One2many('estate.property', 'seller_id', 'User properties',
                                   domain=['|', ('state', '=', 'new'), ('state', '=', 'received')])
