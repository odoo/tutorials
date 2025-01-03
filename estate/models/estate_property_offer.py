from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline Date", 
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline",
        default=datetime.today()
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - datetime.today().date()
                record.validity = delta.days
            else:
                record.validity = 0

    def action_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id


    def action_cancel(self):
        for record in self:
            record.status = 'refused'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id