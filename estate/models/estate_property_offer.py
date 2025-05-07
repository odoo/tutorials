# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status", copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Prospective Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='cascade')

    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        string="Property Type",
        store=True
    )
    creation_date = fields.Date(string="Creation Date", default=fields.Date.today, readonly=True)
    valid_until = fields.Date(string="Valid Until", compute='_compute_valid_until', inverse='_inverse_valid_until', store=True, readonly=False)

    # Computed fields for button visibility
    can_accept = fields.Boolean(string="Can Accept", compute='_compute_can_accept_refuse')
    can_refuse = fields.Boolean(string="Can Refuse", compute='_compute_can_accept_refuse')

    @api.depends('property_id.state', 'status')
    def _compute_can_accept_refuse(self):
        for offer in self:
            parent_state_prevents_action = offer.property_id.state in ('sold', 'canceled', 'offer_accepted')
            offer.can_accept = not parent_state_prevents_action and offer.status != 'accepted'
            offer.can_refuse = not parent_state_prevents_action and offer.status != 'refused'


    @api.depends('creation_date')
    def _compute_valid_until(self):
        for record in self:
            record.valid_until = record.creation_date + relativedelta(days=7) if record.creation_date else False

    def _inverse_valid_until(self):
        for record in self:
            record.creation_date = record.valid_until - relativedelta(days=7) if record.valid_until else False

    _sql_constraints = [('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be positive.')]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals.get('property_id'))
            existing_offer_prices = prop.offer_ids.filtered(lambda o: o.status != 'refused').mapped('price')
            if prop and existing_offer_prices and vals.get('price') < max(existing_offer_prices):
                 raise UserError(f"Cannot create an offer with a price lower than existing non-refused offers for this property.")
        return super().create(vals_list)

    def action_accept_offer(self):
        self.ensure_one()
        if not self.can_accept: # Use computed field for check
             raise UserError("Offer cannot be accepted at this time (check property state or offer status).")
        # Refuse other offers for the same property
        self.property_id.offer_ids.filtered(lambda o: o.id != self.id and o.status != 'refused').action_refuse_offer()
        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        # If this was the accepted offer, reset property state and selling price
        if self.status == 'accepted' and self.property_id.state == 'offer_accepted' and self.property_id.selling_price == self.price and self.property_id.buyer_id == self.partner_id:
            self.property_id.selling_price = 0
            self.property_id.buyer_id = False
            other_non_refused_offers = self.property_id.offer_ids.filtered(lambda o: o.id != self.id and o.status != 'refused')
            if other_non_refused_offers:
                self.property_id.state = 'offer_received'
            else:
                self.property_id.state = 'new'
        self.status = 'refused'
        return True