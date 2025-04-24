from dateutil import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate: Offer"

    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_compute_deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "An offer price must be positive",
        )
    ]

    @api.depends("validity")
    def _compute_deadline(self) -> None:
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = creation_date + relativedelta.relativedelta(days=record.validity)

    def _inverse_compute_deadline(self) -> None:
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_refuse_offer(self) -> bool:
        for record in self:
            record.status = "refused"
            record.property_id.write(
                {
                    "selling_price": None,
                    "buyer_id": None,
                }
            )
        return True

    def action_accept_offer(self) -> bool:
        for record in self:
            record.property_id.offer_ids.filtered(lambda x: x.status == "accepted").write({"status": "refused"})
            record.status = "accepted"
            record.property_id.write(
                {
                    "selling_price": record.price,
                    "buyer_id": record.partner_id,
                }
            )

        return True
