# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date.date() + \
                                fields.date_utils.relativedelta(days=rec.validity) if rec.create_date else None

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date.date()).days \
                if rec.date_deadline and rec.create_date else 7

    def action_accept_offer(self):
        for rec in self:
            if rec.property_id.buyer:
                raise UserError(
                    'This property already has a buyer.'
                )
            rec.status = 'accepted'
            rec.property_id.state = 'offer_accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer = rec.partner_id.id

    def action_refuse_offer(self):
        for rec in self:
            if rec.status == 'accepted':
                rec.property_id.selling_price = 0
                rec.property_id.buyer = False
            rec.status = 'refused'
            rec.property_id.state = 'offer_received'

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Price must be positive."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['price']:
                self.env['estate_property'].browse(vals['property_id']).state = 'offer_received'
                all_offers_for_property = self.env['estate_property_offer']. \
                    search([('property_id', '=', vals['property_id'])])

                if all_offers_for_property:
                    if vals['price'] < max(all_offers_for_property.mapped('price')):
                        raise UserError('The price must be higher than the previous offer.')

        return super().create(vals_list)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     offers = super().create(vals_list)
    #
    #     for offer in offers:
    #         offer.property_id.state = 'offer_received'
    #         all_offers_for_property = offer.property_id.offers_ids - offer
    #         if offer < max(all_offers_for_property.mapped('price')):
    #             raise UserError('The price must be higher than the previous offer.')
    #
    #     return offers
