from odoo import api, fields, models, _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float("Price")
    state = fields.Selection(string="Status", copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    property_id = fields.Many2one("estate.property", string="Property")
    partner_id = fields.Many2one("res.partner", string="Partner")
