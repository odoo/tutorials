from odoo import models, fields

class EstatePpropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer description'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="status string",
        copy=False,
    )

    # offer Many2one relation with res.partner
    partner_id = fields.Many2one(
        'res.partner',
        required=True
    )

    # offer Many2one realtion with property
    property_id = fields.Many2one(
        'estate.property',
        required=True
    )