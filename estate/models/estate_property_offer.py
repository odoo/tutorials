from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real Estate Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)