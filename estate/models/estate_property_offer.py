from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(
        string='Price',
        required=True
    )

    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False
    )

    # Many2one → res.partner (the buyer making the offer)
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    # Many2one → estate.property (which property this offer is for)
    # This is the REQUIRED inverse field for the One2many on the property
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )
