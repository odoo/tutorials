from odoo import fields, models


class res_users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        string='property',
        comodel_name='estate.property',
        inverse_name='salesman_id',
        domain=[('state', 'not in', ['sold', 'cancelled'])],
    )
