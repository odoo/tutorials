from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Bids for a property"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False
        , selection=[('accepted', 'Accepted'), ('refused', 'Refused')])

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
