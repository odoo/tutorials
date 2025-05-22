from datetime import timedelta, datetime
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offer description"

    name = fields.Char('Offer', required=False)
    price = fields.Float('Offer amount', digits=(16, 2))
    status = fields.Selection(
        string='Offer State',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        default='',
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type')

    validity_days = fields.Integer('Validity (Days)')
    deadline = fields.Date('Offer Deadline', compute='_compute_offer_deadline', inverse='_inverse_offer_deadline')

    # Ordering
    _order = "price desc"

    # DB Constraints
    _sql_constraints = [
        ("check_offer_price_is_positive", "CHECK(price > 0)", "The offered price must be positive."),
    ]

    @api.depends('validity_days')
    def _compute_offer_deadline(self):
        for offer in self:
            if not offer.create_date:
                _create_date = fields.Date.today()
            else:
                _create_date = offer.create_date
            offer.deadline = _create_date + timedelta(days=offer.validity_days)

    def _inverse_offer_deadline(self):
        for offer in self:
            if not offer.create_date:
                _create_date = fields.Date.today()
            else:
                _create_date = offer.create_date.date()
            offer.validity_days = (offer.deadline - _create_date).days

    # Actions
    def action_offer_accept(self):
        for offer in self:
            if not offer.status == 'accepted':
                offer.property_id._notify_offer_accepted(offer)
        return True

    def action_offer_refuse(self):
        for offer in self:
            if not offer.status == 'refused':
                offer.property_id._notify_offer_refused(offer)
        return True
