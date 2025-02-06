from odoo import models, fields, api
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"

    _description = "Estate Property Offer"

    _order = "price desc"  # Order by descending price

    price = fields.Float("Price")

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status"
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    create_date = fields.Datetime(readonly=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price=record.price
            record.property_id.buyer_id=record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        # Create the offer first
        offer = super(EstatePropertyOffer, self).create(vals)

        # Once the offer is created, set the property status to "offer_received"
        if offer.property_id:
            offer.property_id.state = "offer_received"

        return offer


