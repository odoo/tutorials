from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Property Offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy="False",
    )
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "Offer price must be positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def set_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id.name = record.partner_id.name
        return True

    def set_refused(self):
        for record in self:
            record.status = "refused"
        return True
