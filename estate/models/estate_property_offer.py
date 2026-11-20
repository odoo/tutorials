from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('Price')
    _check_price = models.Constraint(
        'CHECK(price > 0)', 'The offer price must be strictly positive.'
    )
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        related='property_id.property_type_id',
    )

    def _get_create_date(self):
        return fields.Date.to_date(self.create_date) or fields.Date.today()

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record._get_create_date() + timedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record._get_create_date()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'canceled':
                raise UserError('Canceled properties cannot accept offers.')
            if record.property_id.state == 'sold':
                raise UserError('Sold properties cannot accept offers.')
            if record.property_id.state == 'offer_accepted':
                raise UserError('An offer has already been accepted.')
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env['estate.property'].browse(vals['property_id'])
            if estate_property.offer_ids and vals['price'] <= max(
                estate_property.offer_ids.mapped('price')
            ):
                raise UserError(
                    'The offer price must be greater than the existing offers.'
                )
            if estate_property.state == 'new':
                estate_property.state = 'offer_received'
        return super().create(vals_list)
