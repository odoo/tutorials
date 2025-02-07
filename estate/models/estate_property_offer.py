from odoo import fields, models

class PropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers that property has'

    price = fields.Float()
    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
