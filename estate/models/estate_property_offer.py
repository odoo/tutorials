from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made for an Estate Property'
    _order = 'price desc'
    _sql_constraints = [
        (
            'estate_property_offer_price_positive',
            'CHECK(price > 0)',
            'The offer price must be strictly positive.',
        )
    ]

    price = fields.Float('Price')
    validity = fields.Integer('Validity (days)', default=7)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(
        'Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        related='property_id.property_type_id',
        store=True,
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                relativedelta(
                    record.date_deadline, (record.create_date or fields.Date.today())
                ).days
                + 1
            )

    def action_accept(self):
        for record in self:
            record_property = record.property_id
            property_state = record_property.state

            if property_state == 'offer_accepted':
                raise UserError('You can only accept one offer at a time.')
            if property_state == 'sold':
                raise UserError('You cannot accept an offer on a sold property.')
            if property_state == 'cancelled':
                raise UserError('You cannot accept an offer on a cancelled property.')
            if record.status == 'refused':
                raise UserError('You cannot accept an already refused offer.')

            other_offers = record_property.offer_ids.filtered(
                lambda o: o.id != record.id
            )
            other_offers.write({'status': 'refused'})

            record.status = 'accepted'
            record_property.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
                'state': 'offer_accepted',
            })

        return True

    def action_refuse(self):
        for record in self:
            record_property = record.property_id
            property_state = record_property.state

            if property_state in ['sold', 'cancelled']:
                raise UserError(
                    'You cannot refuse an offer on a sold or cancelled property.'
                )
            if property_state == 'new':
                raise ValidationError(
                    'You cannot refuse an offer on a new property. (New properties are not supposed to have offers.)'
                )
            if record.status == 'accepted':
                raise UserError('You cannot refuse an already accepted offer.')

            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        curr_max_price = 0
        for vals in vals_list:
            estate_property = self.env['estate.property'].browse(vals['property_id'])

            if estate_property.state in ['sold', 'cancelled']:
                raise UserError(
                    'You cannot create an offer on a sold or cancelled property.'
                )
            if curr_max_price >= vals['price']:
                raise UserError(
                    'The offer price must be higher than the current best price.'
                )
            curr_max_price = max(curr_max_price, vals['price'])

            estate_property.state = 'offer_received'
        return super().create(vals_list)
