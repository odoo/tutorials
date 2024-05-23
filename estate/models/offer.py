from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "offer"
    _description = "Offer"
    price = fields.Float(string="Price")
    status = fields.Selection(copy=False, string="Status", selection=[ ("accepted", "Accepted"), ("refused", "Refused")],
                              required=True)
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate_property", string="Estate Property",required=True)
