from odoo import models, fields


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Property Offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy="False",
    )
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
