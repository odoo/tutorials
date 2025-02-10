from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for the property"

    price = fields.Float(
        string="Offer Price",
        help="Price for the offer"
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        help="Current status of the property",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner",
        required=True,
        help="Partner assigned for the sale"
    )
    property_id = fields.Many2one(
        "estate.property", string="Property",
        required=True,
        help="Property for sale"
    )
