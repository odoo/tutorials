# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    state = fields.Selection(copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_dead_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if isinstance(record.create_date, fields.Date):
                record.date_deadline = record.create_date.replace(
                    day=record.create_date.day+record.validity)
            else:
                fields.Date.today()
                record.date_deadline = fields.Date.today().replace(
                    day=fields.Date.today().day+record.validity)

    def _inverse_dead_deadline(self):
        for record in self:
            cd = fields.Date.to_date(record.create_date or fields.Date.today())
            record.validity = (record.date_deadline - cd).days

    def action_accept(self):
        for record in self:
            if record.state != 'accepted':
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'sold'
                record.state = 'accepted'
            else:
                raise exceptions.UserError(
                    'You can’t accept an offer for a sold property')

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
