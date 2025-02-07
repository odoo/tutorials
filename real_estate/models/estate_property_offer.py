from datetime import date, timedelta
from odoo import models, fields, api

class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Offers on Property"

    create_date = fields.Date(
        string="Create Date",
        default=date.today(),
        readonly=True
    )
    price = fields.Float(
        string="Offer Price"
    )
    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
        required=True
    )

    date_deadline = fields.Date(
        string="Deadline Date",
        compute='_compute_date_deadline', 
        inverse='_inverse_date_deadline', 
    )
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days
            elif record.date_deadline:
                record.validity = 7

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
