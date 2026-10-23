from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for an estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date.date()
            record.validity = delta.days

    @api.model
    def create(self, vals_list):
        property_ids = [val["property_id"] for val in vals_list]
        property_by_id = dict(
            zip(
                property_ids,
                self.env["estate.property"].browse(property_ids),
                strict=True,
            ),
        )
        for val in vals_list:
            property = property_by_id[val["property_id"]]
            if (
                float_compare(
                    val.get("price", 0),
                    property.best_price,
                    precision_digits=2,
                )
                <= 0
            ):
                raise UserError(
                    self.env._(
                        "The offer must be higher than %(best_price).2f.",
                        best_price=property.best_price,
                    ),
                )
        offers = super().create(vals_list)
        offers.property_id.state = "received"
        return offers

    def action_accept(self):
        self.ensure_one()
        if self.property_id.offer_ids.filtered(
            lambda offer: offer.status == "accepted",
        ):
            raise UserError(
                self.env._("There is already an accepted offer for this property."),
            )
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"
        return True
