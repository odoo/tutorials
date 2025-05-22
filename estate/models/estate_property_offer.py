from odoo import fields, models, api, exceptions
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ("positive_price", "CHECK(price >= 0)", "The price must be positive."),
    ]

    # Foreign keys
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date.date() if record.create_date else date.today()
            validity_time = timedelta(days=record.validity)
            record.date_deadline = creation_date + validity_time

    def _inverse_deadline(self):
        for record in self:
            creation_date = record.create_date.date() if record.create_date else date.today()
            validity_time = record.date_deadline - creation_date
            record.validity = validity_time.days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ["accepted", "canceled", "sold"]:
                raise exceptions.UserError("Cannot accept an offer for an unavailable property.")

            record.property_id.state = "accepted"
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"

        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise exceptions.UserError("Cannot refuse an offer that was already accepted.")
            record.status = "refused"
        return True
