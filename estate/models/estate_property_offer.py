from odoo import fields,models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
    )
