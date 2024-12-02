from odoo import models, fields


class User(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        domain=[('state', 'in', ('new', 'received'))],
        readonly=True,
    )
