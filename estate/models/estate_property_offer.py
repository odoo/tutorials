from odoo import models, fields  # type: ignore

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string='Status',
    )

    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)