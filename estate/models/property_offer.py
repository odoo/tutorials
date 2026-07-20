import datetime as dt
from math import floor

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Bids for a property"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False
        , selection=[('accepted', 'Accepted'), ('refused', 'Refused')])

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity of offer", default=7)
    date_deadline = fields.Date(string="Offer expiry", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = None
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                raw_difference = record.date_deadline - (record.create_date.date() or fields.Date.today())
                difference = raw_difference.total_seconds()
                if difference > 0:
                    record.validity = floor(difference / dt.timedelta(days=1).total_seconds())
