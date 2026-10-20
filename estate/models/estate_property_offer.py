from dateutil.relativedelta import relativedelta
from odoo import api, fields, models  # ty: ignore[unresolved-import]
from odoo.exceptions import UserError  # ty: ignore[unresolved-import]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property by buyer"
    _order = "price desc"

    price = fields.Float()
    _check_price = models.Constraint(
        "CHECK(price >= 0)", "The offer price must be non-negative"
    )

    status = fields.Selection(
        string="Offer Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    @api.onchange("deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                base_date = (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.context_today(record)
                )
                delta = record.deadline - base_date
                record.validity = max(delta.days, 0)
            else:
                record.validity = record.validity.default

    def confirm_offer(self):
        for record in self:
            if (
                record.property_id.state == "offer_accepted"
                or record.property_id.state == "sold"
                or record.property_id.state == "cancelled"
            ):
                raise UserError(
                    "Cannot accept an offer for a property that has already accepted and offer or is cancelled"
                )
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            if (
                record.status == "accepted"
                and record.property_id.state == "offer_accepted"
            ):
                record.property_id.state = "offer_received"
                record.property_id.buyer = None
                record.property_id.selling_price = None
            record.status = "refused"
        return True
