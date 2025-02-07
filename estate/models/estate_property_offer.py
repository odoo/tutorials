from odoo import models,fields


class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='for adding offers of properties'

    price=fields.Float(string='Price')
    status=fields.Selection(
        string='Status',
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ],
        copy=False
    )
    partner_id=fields.Many2one('res.partner', string='Partner', required=True)
    property_id=fields.Many2one('estate.property', string='Property', required=True)
