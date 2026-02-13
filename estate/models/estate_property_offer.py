from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Esate Property Offer"

    price = fields.Float(string="Price Offered")
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
