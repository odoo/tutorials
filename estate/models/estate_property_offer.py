from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    validity = fields.Integer(default=7)

    _positive_price = models.Constraint(
        "CHECK(price > 0)", "The price of an offer cannot be negative."
    )
    _order = "price desc"

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                fields.Date.to_date(record.create_date)
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                continue
            base_date = (
                fields.Date.to_date(record.create_date)
                if record.create_date
                else fields.Date.today()
            )
            record.validity = (record.date_deadline - base_date).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state not in ["new", "offer_received"]:
                raise UserError(
                    "You can only accept offers for properties that are new or have received offers."
                )
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(
                    "You cannot refuse an offer that has already been accepted."
                )
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(
                vals.get("property_id")
            )
            existing_prices = estate_property.offer_ids.mapped("price")

            if existing_prices:
                min_price = min(existing_prices)
                if (
                    float_compare(vals.get("price", 0.0), min_price, precision_digits=2)
                    < 0
                ):
                    raise UserError(
                        f"The offer {vals.get('price', 0.0)} cannot be lower than the other offers."
                    )
            estate_property.state = "offer_received"

        return super().create(vals_list)
