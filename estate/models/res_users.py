# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ['res.users']
    _name = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'seller_id',
        string="Available Properties",
        domain=[('state', 'in', ['new', 'offer_received'])],
    )
