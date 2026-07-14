from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is estate property offer"
    _order = "price desc"

    price = fields.Float()

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )

    validity = fields.Integer(
        string="Days",
        default=7,
    )

    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The Price should be Positive",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(
                    days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    delta = record.date_deadline - record.create_date.date()
                    record.validity = delta.days
            else:
                record.validity = 7

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            current_price = vals.get('price')
            property_record = self.env['estate.property'].browse(
                vals['property_id'],
            )

            for record in property_record.offer_ids:
                other_price = record.price

                if current_price < other_price:
                    raise UserError("This offer can't be created")

            if property_record.state == "new":
                property_record.state = "offer_received"

        return super().create(vals_list)

    def action_accept(self):

        for offer in self.property_id.offer_ids:
            if self != offer and offer.status == "accepted":
                raise UserError("An offer is already accepted.")

        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"

        return True

    def action_reject(self):
        for record in self:
            record.status = "rejected"

        return True
