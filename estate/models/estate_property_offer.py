from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "name"

    name = fields.Char(required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)