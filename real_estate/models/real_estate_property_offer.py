from odoo import models, fields

class real_estate_property_offer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(string='Price', required=True)
    property_id = fields.Many2one('real.estate', string='Property', ondelete='cascade')
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused'),
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)