from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class PropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers that property has'
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',  inverse="_inverse_date_deadline", string='Deadline')

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price >= 0)', 'Offer price must be strictly positive.'),
        ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            
            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = 'rejected'

    def action_reject(self):
        for record in self:
            record.status = 'rejected'
