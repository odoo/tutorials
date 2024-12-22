# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import timedelta, datetime
from odoo.exceptions import UserError, ValidationError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Manage different offers from buyers for a specific property."
    _order = "price desc"

    price = fields.Float(string="Price", required=True, default=1.0)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline",
                                inverse="_inverse_deadline")

    status = fields.Selection([('accepted', 'Accepted'),
                               ('refused', 'Refused')],
                               copy=False)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price should be greater than zero.')
    ]
                               
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )

    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True
    )

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            if record.get('property_id'):
                curr_prop = self.env['estate.property'].browse(record['property_id'])
                
                if curr_prop.offer_ids:
                    max_offer = max(curr_prop.offer_ids, key=lambda offer: offer.price)
                
                    if record['price'] < max_offer.price:
                        raise UserError(f"The offer must be higher then {max_offer.price}")

                else:
                    curr_prop.set_property_state()
        
        return super().create(vals)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError(_('The offer price should be greater than zero.')) 

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else datetime.now()
            record.validity = (record.date_deadline - create_date.date()).days

    def accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(_('This offer has already been accepted.'))

            offer_prop = record.property_id
            accepted_off = offer_prop.offer_ids.filtered(lambda x: x.status == 'accepted')

            if accepted_off:
                raise UserError(_('This property has already accepted an offer.'))
            
            offer_prop.property_buyer_id = record.partner_id
            offer_prop.selling_price =record.price
            offer_prop.state = 'offer accepted'

            record.status = 'accepted'
        return True
    
    def reject_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.property_buyer_id = False
                record.property_id.selling_price = 0
            record.status = 'refused'
        return True
