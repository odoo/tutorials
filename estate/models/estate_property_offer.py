from odoo import api, fields, models
from odoo.exceptions import UserError
import datetime


class PropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers made by Buyers'

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
        self.ensure_one()
        if not self.property_id.buyer_id:
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = 'offer_accepted'
        else:
            raise UserError('An Offer is already accepted.')
        return True

    def action_refuse(self):
        self.ensure_one()
        if self.partner_id == self.property_id.buyer_id:
            self.property_id.state = 'offer_received'
            self.property_id.selling_price = 0
            self.property_id.buyer_id = None
        self.status = 'refused'
        return True