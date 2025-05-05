from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'users_id',
        string='Seller of',
        domain=[('state', 'in', ('new', 'received'))],
    )
