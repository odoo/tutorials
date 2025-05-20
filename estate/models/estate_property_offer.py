from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offer description"

    name = fields.Char('Offer', required=True)
    price = fields.Float('Offer amount', digits=(16, 2))
    status = fields.Selection(
        string='Offer State',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        default='accepted',
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
