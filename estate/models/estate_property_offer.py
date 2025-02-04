from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        (
            'check_offer_price_positive',
            'CHECK(price > 0)',
            'The offer price must be strictly positive.',
        ),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
            ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    # Override the create method to enforce business rules on offer creation
    @api.model_create_multi
    def create(self, val_list):
        result = []
        for val in val_list:
            property = self.env['estate.property'].browse(val['property_id'])
            if property.state in ['sold', 'cancelled', 'offer_accepted']:
                raise UserError("Offer can be added only for properties in new or offer received states.")

            # Check if the offer is lower than the current highest offer
            max_value = 0
            if property.offer_ids:
                max_value = max(property.offer_ids.mapped('price'))

            if val['price'] < max_value:
                raise UserError("You can't create offer lower than current best offer.")

            # Update property state when a new offer is received
            property.state = 'offer_received'

            # Call the parent create method and store the result
            result.append(super().create(val))
        return result

    def action_accept(self):
        self.ensure_one()
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")

            if record.property_id.state == 'cancelled':
                raise UserError("You cannot accept an offer for a cancelled property.")

            if record.status == 'refused':
                raise UserError(
                    "You cannot accept an offer that has already been refused."
                )

            record.property_id.offer_ids.filtered(lambda offer: offer.id != record.id).write(
                {'status': 'refused'}
            )

            record.status = 'accepted'
            record.property_id.write(
                {
                    'buyer_id': record.partner_id.id,
                    'selling_price': record.price,
                    'state': 'offer_accepted',
                }
            )

    def action_refuse(self):
        self.ensure_one()
        for record in self:
            if record.status == 'refused':
                raise UserError("This offer has already been refused.")

            if record.status == 'accepted':
                raise UserError(
                    "You cannot refuse an offer that has already been accepted."
                )

            if record.property_id.state == 'sold':
                raise UserError("You cannot refuse an offer for a sold property.")

            record.status = 'refused'
