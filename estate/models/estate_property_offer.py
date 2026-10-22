from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this model defines offers"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        "CHECK (price > 0)",
        "An offer price must be strictly positive",
    )

    @api.model
    def create(self, vals_list):
        for val in vals_list:
            property_id = val.get("property_id")

            if not property_id:
                continue

            property = self.env["estate.property"].browse(property_id)
            price = val.get("price", 0)

            if price < property.best_price:
                raise ValidationError(
                    "You cannot create offer lower than an existing offer."
                )

            if property.state != "o_received":
                property.state = "o_received"

        return super().create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Datetime.now()
            ).date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                # using .date() on create_date because it has type of datetime
                date_diff = record.date_deadline - record.create_date.date()
                record.validity = date_diff.days

    def action_offer_accept(self):
        self.ensure_one()
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = "accepted"

    def action_offer_reject(self):
        self.ensure_one()
        self.status = "refused"
