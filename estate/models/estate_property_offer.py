from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], required=True, default="pending")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
