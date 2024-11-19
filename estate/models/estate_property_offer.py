from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"

    price=fields.Float("Price")
    status=fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)
