from odoo import fields, models


class PropertyOffer (models.Model):
    _name = "estate.property.offer"
    _description = "Property Purchase Offers"

    price = fields.Float(string="Price")
    property_id = fields.Many2one("estate.property", string="Property Name", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
