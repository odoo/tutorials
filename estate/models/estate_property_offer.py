from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()

    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])

    partner_id = fields.Many2one("res.partner", string="Buyer")

    property_id = fields.Many2one("estate.property", string="Property")
