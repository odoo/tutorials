from odoo import fields, models, api


class EstateUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'salesman_id',
        string='Sold Properties',
        domain=[('state', 'in', ('new', 'received'))],
    )
