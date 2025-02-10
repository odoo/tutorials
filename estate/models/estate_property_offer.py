# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]
    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"),
        ("refused", "Refused")],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    create_date = fields.Datetime(string="Creation Date", default=fields.Datetime.now)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError("Offer cannot be accepted on sold property")
            for existing_offer in offer.property_id.offer_ids:
                if existing_offer.status == "accepted":
                    raise UserError("Only one offer can be accepted for a property")
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer accepted"

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Accepted offer can not be refused")
            offer.status = "refused"
