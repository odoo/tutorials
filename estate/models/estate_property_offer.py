from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "This is an offer made by a partner to buy the property"

    price = fields.Float(required=True)
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", string = "Partner", required=True)
    property_id = fields.Many2one("estate.property", "Property", required=True)
