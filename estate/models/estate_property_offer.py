from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("rejected", "Rejected")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")

    property_id = fields.Many2one("estate.property", required=True, string="Property")
