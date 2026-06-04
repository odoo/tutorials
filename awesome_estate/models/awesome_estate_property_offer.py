from odoo import fields, models


class AwesomeEstatePropertyOffer(models.Model):
    _name = 'awesome.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc, id desc'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True,
    )
    property_id = fields.Many2one(
        'awesome.estate.property',
        string='Property',
        required=True,
        ondelete='cascade',
        index=True,
    )
