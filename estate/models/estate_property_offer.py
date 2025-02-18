# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property'
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]

    price = fields.Float(string='Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one(
        'estate.property', required=True, ondelete='cascade')
    create_date = fields.Date()
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        related='property_id.property_type_id',
        store=True
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + \
                    timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                dayys = (offer.date_deadline - offer.create_date).days
                offer.validity = dayys

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property_id = record.get('property_id')
            if property_id:
                existing_offer = self.search(
                    [('property_id', '=', property_id)], limit=1, order='price DESC')
                if existing_offer and existing_offer.price >= vals_list[0]['price']:
                    raise UserError(
                        'You cannot create an offer lower than or equal to an existing offer.')
        records = super().create(vals_list)
        for record in records:
            if record.property_id.state == 'new':
                record.property_id.state = 'offer_received'

            record.property_id.message_post(
                body=f"A new offer of {record.price} has been received by {record.partner_id.name}.",
                subject="New Offer Received",
                message_type="notification",
                subtype_xmlid="mail.mt_comment",
            )
        return records

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError(
                    'You cannot accept an offer for a sold property.')
            existing_accepted_offer = offer.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted')
            if existing_accepted_offer:
                raise UserError(
                    'Only one offer can be accepted for a given property.')
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = 0.00
            offer.property_id.buyer_id = False
            if offer.property_id.state == 'offer_received':
                offer.property_id.state = 'new'
