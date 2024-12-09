from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refussed', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", String="Partener", required=True)
    property_id = fields.Many2one("estate.property", String="Property Id", required=True)