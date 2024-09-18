from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers to estate properties"

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], "Status", required=False, copy=False)
    property_id = fields.Many2one("estate.property", "Property", required=True)
