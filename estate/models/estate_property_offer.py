from dateutil import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate: Offer"
    _order = "price desc"

    price = fields.Float("Price", required=True)
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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "An offer price must be positive",
        )
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = creation_date + relativedelta.relativedelta(days=record.validity)

    def _inverse_compute_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_id = self.env["estate.property"].browse(val["property_id"])
            max_price = max(
                property_id.offer_ids.mapped("price"),
                default=0.0,
            )
            if (
                float_compare(
                    max_price,
                    val["price"],
                    precision_digits=2,
                )
                >= 0
            ):
                raise UserError(_("The offer must be higher than the highest offer."))
            property_id.write({"state": "offer_received"})
        return super().create(vals_list)

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
            record.property_id.write(
                {
                    "selling_price": record.price,
                    "buyer_id": None,
                }
            )
        return True

    def action_accept_offer(self):
        for record in self:
            record.property_id.offer_ids.write({"status": "refused"})
            record.status = "accepted"
            record.property_id.write(
                {
                    "selling_price": record.price,
                    "buyer_id": record.partner_id,
                    "state": "offer_accepted",
                }
            )

        return True
