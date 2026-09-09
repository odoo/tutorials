from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "this model is used to define the offers received to the property"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
