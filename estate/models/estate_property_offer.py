from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type",
        related="property_id.property_type_id", stored=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline",
        compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive."),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = relativedelta(days=record.validity) + (
                    record.create_date if record.create_date else fields.Date.today()
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.id != record.id and offer.status == "accepted":
                    raise UserError(_("Another offer has already been accepted."))

            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "offer_received"
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = None

            record.status = "refused"
