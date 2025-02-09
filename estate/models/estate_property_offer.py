from odoo import fields,models

class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "offers available to property"

    price = fields.Float("Price")
    status = fields.Selection(string = "Status", copy = False, selection = [("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
