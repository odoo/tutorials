from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(
        string='Price',
    )
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
        string='Status',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        string='Partner',
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
        string='Property',
    )
