from odoo import models, fields, api
from datetime import datetime, timedelta

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'my estate property offer'

    price = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending'),
        ],
        default='pending',
        copy=False,
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = start_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - start_date).days