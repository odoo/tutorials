from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)

    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', "Refused"),
        ],
        string="Status",
        copy=False
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer Name",
        required=True
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
