# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
  _name = 'estate.property.offer'
  _description = 'estate property offer'

  price = fields.Float(string='Price')
  status = fields.Selection(
    string='Status',
    copy='False',
    selection=[
      ('accepted', 'Accepted'),
      ('refused', 'Refused')
    ]
  )
  partner_id = fields.Many2one('res.partner', string='Partner', required=True)
  property_id = fields.Many2one('estate.property', string='Property ID', required=True)
  validity = fields.Integer(string='Validity (days)', default=7)
  date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
  property_type_id = fields.Many2one('estate.property.type', string='Property Type', related='property_id.property_type_id')


  @api.depends('validity', 'date_deadline')
  def _compute_deadline(self):
    for record in self:
      record.date_deadline = date.today() + timedelta(days = record.validity)

  def _inverse_deadline(self):
    for record in self:
      record.validity = max((record.date_deadline - date.today()).days, 0)

  @api.model_create_multi
  def create(self, vals_list):
    for vals in vals_list:
      property_record = self.env['estate.property'].browse(vals.get('property_id'))
      new_offer_price = vals.get('price', 0.0)

      if new_offer_price < property_record.best_price:
        raise UserError('You cannot create an offer lower than an existing best offer.')

      if property_record.state == 'new':
        property_record.state = 'offer received'

    return super().create(vals_list)

  _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0.00)',
         'The Offer price must be Positive.')
    ]  

  def action_accepted(self):
    for record in self:
      accepted_offer = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')
      if accepted_offer:
        first_accepted_offer = accepted_offer[0]
        raise UserError(f'An offer with {first_accepted_offer.partner_id.name} at a price of {first_accepted_offer.price} has already been accepted.')

      record.status = 'accepted'
      record.property_id.state = 'offer accepted'
      record.property_id.buyer_id = record.partner_id
      record.property_id.selling_price = record.price

  def action_refused(self):
    for record in self:
      if record.status == 'accepted':
        record.property_id.selling_price = 0.00
        record.property_id.buyer_id = False
        record.property_id.state = 'new'

      record.status = 'refused'
