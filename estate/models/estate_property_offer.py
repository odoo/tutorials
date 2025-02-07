from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "All the available offer for the property"

    property_id = fields.Many2one("estate.property", required=True)
    price = fields.Float(string='Price', required=True)
    buyer_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        string="Status",
        required=True,
        default="accepted",
        copy=False,
        selection=[
            ("refuse", "Refuse"),
            ("accepted", "Accepted")
        ],
    )
