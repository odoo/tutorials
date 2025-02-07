from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Model for Property Offers where one property can have multiple offers'

    price = fields.Float(
        string="Offer Price",
        required=True,
        help="The price offered by the buyer for the property"
    )
    
    status = fields.Selection(
        selection=[
            ('accept', "Accepted"),
            ('reject', "Rejected")
        ],
        string="Status",
        copy=False,
        default='accept',
        help="The current status of the offer"
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True,
        help="The partner (buyer) who made the offer"
    )
    
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True,
        help="The property for which the offer is made"
    )
    
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Number of days the offer is valid"
    )
    
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        help="The deadline for the offer, computed as create_date + validity"
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Computes date_deadline as create_date + validity days"""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        """Sets validity based on date_deadline - create_date"""
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_confirm(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accept' and o != record):
                raise UserError("Only one offer can be accepted per property.")
            record.status = 'accept'
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price

    def action_reject(self):
        for record in self:
            if not record.status:
                record.status='reject'
