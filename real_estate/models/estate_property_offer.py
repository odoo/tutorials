from odoo import models, fields

class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = 'Offers on Property'

    price = fields.Float(
        string="Offer Price"
    )

    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string = "Status",
        copy=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True
    )
    
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )
