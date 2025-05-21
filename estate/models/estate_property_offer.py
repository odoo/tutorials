from datetime import timedelta, datetime

from dateutil.utils import today

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offer description"

    name = fields.Char('Offer', required=False)
    price = fields.Float('Offer amount', digits=(16, 2))
    status = fields.Selection(
        string='Offer State',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        default='accepted',
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    # Chapter 8
    validity_days = fields.Integer('Validity (Days)')
    deadline = fields.Date('Offer Deadline', compute='_compute_offer_deadline', inverse='_inverse_offer_deadline')

    @api.depends('validity_days')
    def _compute_offer_deadline(self):
        for offer in self:
            if not offer.create_date:
                _create_date = fields.Date.today()
            else:
                _create_date = offer.create_date
            offer.deadline = _create_date + timedelta(days=offer.validity_days)

    def _inverse_offer_deadline(self):
        print("inverse_offer_deadline got called")
        for offer in self:
            if not offer.create_date:
                _create_date = fields.Date.today()
            else:
                _create_date = offer.create_date.date()
            offer.validity_days = (offer.deadline - _create_date).days
