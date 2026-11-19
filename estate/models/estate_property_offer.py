from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ESTATE property tag"

    currency_id = fields.Many2one(
        "res.currency",
        related="property_id.currency_id")
    price = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
