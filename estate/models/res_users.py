from odoo import _, fields, models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property', 'salesman_id', string='Property',
        domain=[('state', 'not in', ['cancelled', 'sold'])]
    )
