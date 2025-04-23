from odoo import fields, models


class Offer(models.Model):
    _name = "offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    buyer_id = fields.Many2one("buyer")
    property_id = fields.Many2one("realestate")
