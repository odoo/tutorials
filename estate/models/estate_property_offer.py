from odoo import models, fields


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer for each property."

    price = fields.Float()
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
