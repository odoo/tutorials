from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float('Price', digits=(12, 2), required=True)
    partner = fields.Many2one("res.partner", string='Partner', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    property_id = fields.Many2one("estate.property", "property_id", required=True, readonly=True)
