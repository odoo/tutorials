from odoo import api, fields, models
from odoo.exceptions import UserError

import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on estate property"

    price = fields.Float('Price')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True)
    property_id = fields.Many2one('estate.property', string='Property', copy=False, required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline Date', compute='_compute_deadline', inverse='_inverse_deadline')
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        default='new',
    )

    _sql_constraints = [
        ('price', 'CHECK(price > 0)', 'Prices must be strictly positive.'),
    ]

    _order = "price desc"

    def action_set_accepted(self):
        if 'accepted' in self.property_id.offer_ids.mapped('state'):
            raise UserError('Another offer has already been accepted')
        
        self.property_id.partner_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

        self.state = 'accepted'

        return True

    def action_set_refused(self):
        self.state = 'refused'

        return True

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + datetime.timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
