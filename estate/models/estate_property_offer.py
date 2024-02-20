from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate."

    price = fields.Float(string="Price")

    status = fields.Selection(
            string="Status",
            copy=False,
            selection=[("accepted", "Accepted"), ("refused", "Refused")])

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    property_id = fields.Many2one(
            "estate.property", string="Property", required=True)
