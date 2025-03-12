from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('sold', 'Sold'),
        ('refused', 'Refused'),
    ], string="Status", default="new")

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    validity= fields.Integer(string="Valid", default=7)
    date_deadline= fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline",string="Offer Deadline ", default=date.today()+relativedelta(days=7))

    _sql_constraints = [
        ('check_price', 'CHECK(price > )',
         'An offer price must be strictly positive')
    ]

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date.date() + relativedelta(days=+(record.validity))

    def accept_offer(self):
        for record in self:
            record.state = "accepted"
            record.property_id.selling_price=record.price
            record.property_id.buyer_id=record.partner_id

            other_offers = record.property_id.offer_ids - record
            other_offers.write({'state': 'refused'})
        return True

    def refuse_offer(self):
        for record in self:
            record.state = "refused"
            record.property_id.selling_price=0
            record.property_id.buyer_id=False

        return True