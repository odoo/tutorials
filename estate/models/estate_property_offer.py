from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('Price')
    state = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record._get_create_date() + timedelta(
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record._get_create_date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env['estate.property'].browse(vals['property_id'])
            if estate_property.offer_ids and vals['price'] <= max(
                estate_property.offer_ids.mapped('price'),
            ):
                msg = 'The offer price must be greater than the existing offers.'
                raise UserError(msg)
            if estate_property.state == 'new':
                estate_property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'canceled':
                msg = 'Canceled properties cannot accept offers.'
                raise UserError(msg)
            if record.property_id.state == 'sold':
                msg = 'Sold properties cannot accept offers.'
                raise UserError(msg)
            if record.property_id.state == 'offer_accepted':
                msg = 'An offer has already been accepted.'
                raise UserError(msg)
            record.state = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.state = 'refused'
        return True

    def _get_create_date(self):
        return fields.Date.to_date(self.create_date) or fields.Date.today()
