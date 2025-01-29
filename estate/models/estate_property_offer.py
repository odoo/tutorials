from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
