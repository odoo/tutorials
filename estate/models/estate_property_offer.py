from odoo import models, fields


class Estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Offer for estate properties"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    state = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], string="State", copy=False)
