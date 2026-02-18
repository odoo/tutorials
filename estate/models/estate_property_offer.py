from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True
    )

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.'
    )
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            start = fields.Date.to_date(offer.create_date) or fields.Date.today()
            offer.date_deadline = fields.Date.add(start, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start = fields.Date.to_date(offer.create_date) or fields.Date.today()
            if offer.date_deadline and start:
                delta = offer.date_deadline - start
                offer.validity = delta.days

    def accept_offer(self):
        for offer in self:
            # Check no other offer has been accepted for the same property
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError('Another offer has already been accepted for this property.')
        
            # Accept the offer
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id

            # Refuse all other offers for the same property
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id and o.status != 'refused')
            for other_offer in other_offers:
                other_offer.status = 'refused'

    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            if offer.property_id.state != 'offer_accepted':
                offer.property_id.state = 'offer_received'
