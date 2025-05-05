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

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = self.env["estate.property"].browse(val["property_id"])

            if property_id.status in ["cancelled", "sold"]:
                raise UserError("Cannot submit an offer on a cancelled or a sold property.")

            if property_id.best_offer_price > val["price"]:
                raise UserError("Cannot submit an offer with a price lower than the best offer price.")

            property_id.write({"status": "offer_receieved"})

        return super().create(vals)

    def unlink(self):
        property_ids = set()

        for record in self:
            property_ids.add(record.property_id.id)

        deletion_state = super().unlink()

        for property_id in property_ids:
            offers_cnt = self.env["estate.property.offer"].search_count([("property_id", "=", property_id)])
            if not offers_cnt:
                self.env["estate.property"].browse(property_id).write({"status": "new"})

        return deletion_state

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

        has_offer_accepted = self.property_id.status == "offer_accepted"

        if has_offer_accepted:
            raise UserError(f"Property with name {self.property_id.name} has an accepted offer.")

        self.status = "accepted"
        self.property_id.status = "offer_accepted"

    def action_reject_offer(self):
        for record in self:
            if record.status == "accepted" and record.property_id.status == "sold":
                raise UserError(f"Property with name {record.property_id.name} has already been sold.")

            record.status = "rejected"
