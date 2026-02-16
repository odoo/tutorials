from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                base_date = (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.today()
                )
                record.validity = (record.date_deadline - base_date).days

    def action_accept_offer(self):
        for record in self:
            # Check if another offer already accepted
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if accepted_offer:
                raise UserError("Another offer is already accepted for this property.")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False

            record.status = "refused"
        return True
