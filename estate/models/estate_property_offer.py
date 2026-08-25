from odoo import fields, models, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
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
        string="Validity (days)",
        default=7,
    )
    deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        "CHECK(price>0)",
        "Offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.deadline:
                record.validity = (record.deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

        for offer in record.property_id.offer_ids:
            if offer.status != "accepted":
                offer.status = "refused"

    def action_cancel(self):
        for record in self:
            record.status = "refused"
