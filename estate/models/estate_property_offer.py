import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers made by Buyers'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string='Offer state',
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False,
        readonly=True
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)', 'Offer price must be strictly positive')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.today(),days=record.validity)
            else:
                record.date_deadline = fields.Date.add(record.create_date,days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Date.from_string(record.create_date)
                record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for record in self:
            if not record.property_id.buyer_id and record.property_id.state in ['new','offer_received']:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'
            else:
                raise UserError('An Offer is already accepted.')
        return True

    def action_refuse(self):
        for record in self:
            if record.partner_id == record.property_id.buyer_id:
                record.property_id.selling_price = 0
                record.property_id.buyer_id = None
            elif record.property_id.state == 'offer_accepted':
                record.property_id.state = 'offer_accepted'
            else:
                record.property_id.state = 'offer_received'
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = self.env['estate.property'].browse(val['property_id'])
            offer_price = val.get('price')
            if property_id.state in ['sold','canceled','offer_accepted']:
                raise UserError('Can not make an offer on sold or canceled or offer accepted properties')
            elif property_id.best_price <= offer_price:
                property_id.state = 'offer_received'
            else:
                raise UserError('An offer with amount greater than this is already made, please consider increasing the amount')
        return super().create(vals)
