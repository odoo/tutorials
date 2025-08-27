# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status Of Offer',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
