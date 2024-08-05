from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Offer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
