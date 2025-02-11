# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        if self.status == 'accepted':
            raise UserError("Offer has already been accepted!")
        self.write({'status':'accepted'})
        for property in self.mapped('property_id'):
            property.write({
                'state': 'offer_accepted',
                'selling_price': self.price,
                'buyer_id': self.partner_id,
            })

    def action_refuse(self):
        if self.status == 'refused':
            raise UserError("Offer has already been refused!")
        self.write({'status':'refused'})
