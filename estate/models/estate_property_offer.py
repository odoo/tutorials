# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order = "price desc"
 
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id.id)
    price = fields.Monetary(string="Price")
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused'),
    ], string="Status", copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property ID")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0.0)', 'The Offer price must be strictly positive'),
    ]

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
           record.date_deadline = fields.Date.add((record.create_date or fields.date.today()), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    def action_accepted(self):
        existing_accepted_offer = self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
        if existing_accepted_offer:
            if self.price > existing_accepted_offer.price:
                existing_accepted_offer.status = 'refused'
                self.status = 'accepted'
                self.property_id.state = 'offer_accepted'
                self.property_id.buyer_id = self.partner_id
                self.property_id.selling_price = self.price
            else:   
                raise UserError(_("One offer can only be accepted at a time"))
        else:
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
        return True
    
    def action_refused(self):
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            property_rec = self.env['estate.property'].browse(vals.get('property_id', False))
            if(property_rec.state == 'sold' or property_rec.state == 'offer_accepted'):
                raise UserError(_("Can't add offer for a property that is already in '%s' state." % property_rec.state.replace('_', ' ')))
            property_rec.state = 'offer_received'
            if vals.get('price', 0) < property_rec.best_price:
                raise UserError(_("The new offer price must be higher than the current best offer %.2f." % property_rec.best_price))
        return super().create(vals_list)
