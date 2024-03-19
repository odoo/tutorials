from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False, string="Status")

    partner_id = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property_id = fields.Many2one(string="Property", comodel_name="estate.property", required=True)
