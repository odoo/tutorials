from ast import Store
from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for properties"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted',"Accepted"),
            ('refused',"Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline =  record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        self._inverse_date_deadline()

    def action_offer_accept_button(self):
        for record in self:
            if record.status != 'accepted' and record.property_id.selling_price == 0:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'

        return True

    def action_offer_refuse_button(self):
        for record in self:
            if record.status == 'accepted':
                record.status = 'refused'
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
                record.property_id.state = 'offer_recevied'
            else:
                record.status = 'refused'
        return True

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be greater than zero!')
    ]
