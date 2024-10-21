from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate offers"
    _order = "price desc"

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    partner_id = fields.Many2one("res.users", string="Partner", copy=False)
    status = fields.Selection(
        string="Status",
        selection=[
            ("pending", "Pending"),
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        required=True,
        copy=False,
        default="pending",
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price >= 0)",
            "Offer price must be positive.",
        ),
        (
            "check_partner",
            "CHECK(partner_id != NULL)",
            "Who made this offer ?",
        ),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = int(
                (
                    record.deadline
                    - (
                        record.create_date.date()
                        if hasattr(record, "create_date")
                        else fields.Date.today()
                    )
                ).days
            )

    # TODO: Manage dynamic changes
    @api.constrains("status")
    def _offer_validation_constrain(self):
        if self.status == "accepted":
            for offer in self.property_id.offers_id:
                if offer != self and offer.status == "accepted":
                    raise ValidationError("Another offer has already been accepted.")

            for order_to_refuse in self.property_id.offers_id:
                if order_to_refuse != self:
                    order_to_refuse.status = "refused"

            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

    def action_accept_offer(self):
        self.status = "accepted"
        return True

    def action_reject_offer(self):
        self.status = "refused"
        return True
