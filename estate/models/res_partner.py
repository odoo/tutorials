from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    estate_property_ids = fields.One2many(
        'estate.property',
        'buyer_id',
        "Estate properties"
    )
