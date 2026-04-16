from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    seller_property_ids = fields.One2many(
        'estate.property',
        'seller_id',
        string="Properties",
        domain=[('state', 'in', ['new', 'offer_received'])],
    )
