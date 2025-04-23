from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Property Offers"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate_property", "Property", required=True)
