from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", required=True
    )
    validity = fields.Integer(
        default=7,
        help="offer validity period in days; the offer will be automatically refused when this expires.",
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        default=fields.Date.today() + timedelta(days=7),
        store=True,
    )

    _sql_constraints = [
        (
            "check_property_offer_price",
            "CHECK(price > 0)",
            "Property Offer Price must be a valid value",
        )
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                (record.create_date or fields.date.today()), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                (record.date_deadline - record.create_date.date()).days
                if record.date_deadline
                else 0
            )

    def action_offer_confirm(self):
        if self.status in ["accepted", "refused"]:
            raise UserError(f"Offer is already {self.status}")

        # update the current selected offer
        self.status = "accepted"
        self.property_id.write(
            {
                "buyer": self.partner_id,
                "selling_price": self.price,
            }
        )

        # update the rest offers status to "refused"
        refused_offers = self.property_id.offer_ids - self
        refused_offers.write(
            {
                "status": "refused",
            }
        )

    def action_offer_cancel(self):
        for record in self:
            if record.status in ["accepted", "refused"]:
                raise UserError(f"Offer is already {record.status}")
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property = self.env["estate.property"].browse(record["property_id"])

            if record.get("price") < property.best_price:
                raise UserError(
                    "The offers price cannot be lower than the existing offers"
                )

            property.state = "offer_received"
        return super().create(vals)

    @api.model
    def _cron_refuse_expired_offer_scheduler(self):
        today = fields.Date.context_today(self)
        expired_offer = self.search(
            [("date_deadline", "<=", today), ("status", "=", False)]
        )

        if expired_offer:
            expired_offer.write({"status": "refused"})
