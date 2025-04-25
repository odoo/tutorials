# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "property_offer"
    _description = "Property Offer Model"
    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadine", inverse="_inverse_date_deadline"
    )
    status = fields.Selection(
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The offer price must be positive.")
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadine(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()

            record.date_deadline = record.create_date + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()

            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            accepted_offer_count = self.search_count(
                [
                    ("property_id", "=", record.property_id.id),
                    ("status", "=", "accepted"),
                    ("id", "!=", record.id),
                ]
            )
            if accepted_offer_count > 0:
                raise ValidationError(
                    "There is already an accepted offer for this property"
                )
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
            if record.property_id.selling_price == record.price:
                record.property_id.selling_price = 0
