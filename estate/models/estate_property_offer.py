# estate_property_offer.py
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_id = fields.Many2one('estate.property', 'Property', required=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # Convert create_date to date before subtracting
                create_date_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date_date).days
            else:
                record.validity = 0

    def action_confirm(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("This offer has already been accepted.")
            record.status = 'accepted'
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted',
            })

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    def action_cancel(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("This offer has already been refused.")
            record.status = 'refused'
