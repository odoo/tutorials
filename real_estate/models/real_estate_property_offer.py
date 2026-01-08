from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on Buy or Sell for properties"

    price = fields.Float()
    status = fields.Selection(
        [
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
