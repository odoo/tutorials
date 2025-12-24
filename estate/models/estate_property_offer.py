from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    validity = fields.Integer(default=7, string="Validity (days)")

    # Relations
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # Computed
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_deadline(self) -> None:
        for record in self:
            ref_date = fields.Date.context_today(self) if not record.create_date else record.create_date.date()
            record.date_deadline = ref_date + relativedelta(days=record.validity)

    def _inverse_deadline(self) -> None:
        for record in self:
            ref_date = fields.Date.context_today(self) if not record.create_date else record.create_date.date()
            record.validity = (record.date_deadline - ref_date).days

    # CRUD overrides
    @api.model
    def create(self, vals):
        # This logic is outside the loop to avoid multiple calls to browse if vals contains offers for multiple properties
        property_ids = [val["property_id"] for val in vals]
        estate_properties_by_id = self.env["estate.property"].browse(property_ids).grouped("id")

        for val in vals:
            estate_property = estate_properties_by_id[val["property_id"]]
            best_price = estate_property.best_price or 0.0
            if float_compare(val["price"], best_price, precision_digits=2) < 0:
                raise UserError(self.env._("A new offer must match or exceed the price of the current best offer."))
            estate_property.state = "offer_received"
        return super().create(vals)

    # Public methods
    def action_accept(self) -> bool:
        for record in self:
            if record.status == "accepted":
                continue

            if record.status == "refused":
                raise UserError(record.env._("Cannot accept this offer because it has already been refused."))

            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError(record.env._("Cannot accept this offer because the property has already been sold or cancelled."))

            if record.property_id.offer_ids.filtered(lambda r: r.status == "accepted"):
                raise UserError(record.env._("Cannot accept this offer because another offer has already been accepted for the property."))

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self) -> bool:
        for record in self:
            if record.status == "refused":
                continue

            if record.status == "accepted":
                raise UserError(record.env._("Cannot refuse this offer because it has already been accepted."))

            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError(record.env._("Cannot refuse this offer because the property has already been sold or cancelled."))

            record.status = "refused"
        return True

    # Constraints
    _check_price_strict_positive = models.Constraint(
        "CHECK(price > 0)",
        "An offer's price must be strictly greater than 0.",
    )
