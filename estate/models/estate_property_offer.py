from odoo import api, exceptions, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class Estate_Property_Offer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float(string="Price")

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        readonly=True,
        copy=False,
        string="Status",
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")

    property_id = fields.Many2one("estate_property", string="Property")

    property_type_id = fields.Many2one(
        "estate_property_type", related="property_id.type_id"
    )

    validity = fields.Integer(default=7, string="Validity (days)")

    deadline = fields.Date(compute="_compute_deadline", copy=False, string="Deadline")

    _sql_constraints = [
        (
            "check_positive_price",
            "CHECK(price > 0.0)",
            "Offer Price should be a positive number (higher than 0).",
        )
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = date.today() + relativedelta(days=+record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = relativedelta(date.today(), record.deadline)

    def action_accept(self):
        for record in self:
            if not any(
                offer_status == "accepted"
                for offer_status in record.property_id.offer_ids.mapped("status")
            ):
                # Set values in the Property itself
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.status = "offer_accepted"

                record.status = "accepted"
            else:
                raise exceptions.UserError("An offer has already been accepted.")
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                # Set values in the Property itself
                record.property_id.selling_price = 0.0
                record.property_id.buyer = None
                record.property_id.status = "offer_received"
            record.status = "refused"
        return True

    @api.model
    def create(self, vals):
        _property = self.env["estate_property"].browse(vals["property_id"])
        if vals["price"] < _property["best_offer"]:
            raise exceptions.ValidationError(
                r"Cannot offer less than the best pending offer."
            )
        if _property["status"] == "new":
            _property["status"] = "offer_received"
        return super().create(vals)
