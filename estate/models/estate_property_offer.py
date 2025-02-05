from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This contains offer related configurations."

    price = fields.Float(string="Offer", required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accept", "Accepted"), 
            ("refuse", "Refused"), 
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
