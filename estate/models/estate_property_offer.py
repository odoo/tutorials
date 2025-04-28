import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("rejected", "Rejected"), ("pending", "Pending")],
        default="pending",
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity_days = fields.Integer(default=7)
    deadline_date = fields.Date(compute="_compute_deadline_date", inverse="_inverse_validity_days")

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price of a property must be strictly positive.",
        ),
    ]

    @api.model_create_single
    def create(self, vals):
        record = super().create(vals)
        record.property_id.status = "offer_receieved"
        return record

    @api.depends("validity_days")
    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = datetime.date.today() + datetime.timedelta(days=record.validity_days)

    def _inverse_validity_days(self):
        for record in self:
            record.validity_days = (record.deadline_date - datetime.date.today()).days

    def action_accept_offer(self):
        self.ensure_one()
        if self.property_id.status == "sold":
            raise UserError(f"Property with name {self.property_id.name} has already been sold.")

        has_offer_accepted = self.env["estate.property.offer"].search_count(
            [("status", "=", "accepted"), ("property_id", "=", self.property_id.id)], limit=1
        )

        if has_offer_accepted:
            raise UserError(f"Property with name {self.property_id.name} has an accepted offer.")

        self.status = "accepted"
        self.property_id.status = "offer_accepted"

    def action_reject_offer(self):
        for record in self:
            if record.status == "accepted" and record.property_id.status == "sold":
                raise UserError(f"Property with name {record.property_id.name} has already been sold.")

            record.status = "rejected"
