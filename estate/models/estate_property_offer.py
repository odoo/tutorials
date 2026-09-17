from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on a Real Estate Property"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )

    partner_id = fields.Many2one("res.partner", string="Made by", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
