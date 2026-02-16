from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer description"

    price = fields.Float(string="Price")
    property_offer_ids = fields.Integer(string="Offer")
    state = fields.Selection(
        string="Status",
        copy=False,
        selection=[("acepted", "Accepted"), ("refused", "Refused")],
    )

    salesman_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
