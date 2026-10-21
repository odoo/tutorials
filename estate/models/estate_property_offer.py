# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _explanation = "Defines an offer on real estate property"
    _order = "status"

    price = fields.Float('Price', required=True)
    status = fields.Selection(
        string='Status',
        selection=[('offer_accepted', 'Accepted'), ('offer_refused', 'Refused')],
        copy=False,
        help="Status of the offer")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
