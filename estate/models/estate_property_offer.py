from odoo import fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
