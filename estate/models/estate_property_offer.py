from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='price', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        string="Status",
        copy=False,
        default='accepted',
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
