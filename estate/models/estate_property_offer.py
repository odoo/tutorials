from odoo import api, fields, models
from odoo.exceptions import UserError

import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on estate property"

    price = fields.Float('Price')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True)
    property_id = fields.Many2one('estate.property', string='Property', copy=False, required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', required=True)
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
        for offer in self:
            if 'accepted' in offer.property_id.offer_ids.mapped('state'):
                raise UserError('Another offer has already been accepted')
            
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'

            offer.state = 'accepted'

        return True

    def action_set_refused(self):
        for offer in self:
            offer.state = 'refused'

        return True

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + datetime.timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            property_id.state = 'offer_received'

            if property_id.best_offer > vals['price']:
                raise UserError("Can't create an offer whose price is lower than another offer")

        return super().create(vals_list)
