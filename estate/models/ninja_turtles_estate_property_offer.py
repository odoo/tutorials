from odoo import models, fields


class NinjaTurtlesEstatePropertyOffer(models.Model):
    _name = "ninja.turtles.estate.property.offer"
    _description = "Ninja Turtles Estate for faster Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )
    property_id = fields.Many2one(
        "ninja.turtles.estate",
        string="Property",
        required=True
    )
