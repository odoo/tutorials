from odoo import models, fields, api
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer"
    price = fields.Float()
    _order = "sequence, price desc"
    sequence = fields.Integer("Sequence")
    _sql_constraints = [
        ("offer_price", "CHECK(price > 0)", "offer price must be strictly positive")
    ]
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline"
    )
    property_type_id = fields.Many2one(related="property_id.property_type", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            today = record.create_date
            if today:
                today = record.create_date
            else:
                today = date.today()
            if record.date_deadline:
                record.date_deadline = today + (
                    record.validity - (record.date_deadline - today).days
                )
            else:
                record.date_deadline = timedelta(days=record.validity) + today

    def _inverse_deadline(self):
        for record in self:
            today1 = fields.Date.from_string(record.create_date)
            updated_deadline_date = fields.Date.from_string(record.date_deadline)
            record.validity = (updated_deadline_date - today1).days

    @api.ondelete(at_uninstall=False)
    def _deletion_check(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0

    def action_confirm(self):
        if self.property_id.buyer_id:
            raise UserError("Validation Error!, It is already accepted")
        else:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.status = "accepted"
            self.property_id.state = "offer_accepted"

    def action_refused(self):
        if self.status == "accepted" and self.property_id.buyer_id == self.partner_id:
            self.status = "refused"
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0
            self.property_id.state = "new"
        else:
            self.status = "refused"

    @api.model
    def create(self, vals):
        property_record = self.env["estate.property"].browse(vals.get("property_id"))
        if not property_record:
            raise ValidationError("record not found")
        existing_offers = self.search([("property_id", "=", vals.get("property_id"))])
        highest_offer = 0
        for offer in existing_offers:
            if offer.price >= highest_offer:
                highest_offer = offer.price
        # Check if the new offer amount is lower than the highest existing offer
        if vals.get("price") < highest_offer:
            raise ValidationError(
                "The new offer amount must be higher than the existing highest offer."
            )
        if property_record.state != "offer_received":
            property_record.state = "offer_received"
        return super().create(vals)
