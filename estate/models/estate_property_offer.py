from odoo import models, fields

PROPERTY_OFFER_STATE = [("accepted", "Accepted"), ("refused", "Refused")]
class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=PROPERTY_OFFER_STATE, copy=False)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
