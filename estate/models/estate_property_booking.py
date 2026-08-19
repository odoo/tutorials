from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Property Booking Details"

    name = fields.Char(
        string="Booking Details",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: "New",
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True
    )
    seller_id = fields.Many2one(
        related="property_id.salesperson_id.partner_id",
        string="Seller",
        store=True,
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
    )
    booking_date = fields.Date(
        default=fields.Date.today,
    )
    final_price = fields.Float(
        related="property_id.selling_price",
        required=True
    )
    booking_amount = fields.Float(
        compute="_compute_booking_amount",
        store=True,
    )
    remaining_amount = fields.Float(
        compute="_compute_remaining_amount",
        store=True,
    )
    payment_mode = fields.Selection(
        [
            ("cash", "Cash"),
            ("upi", "UPI"),
            ("cheque", "Cheque"),
        ],
        string="Payment Mode",
    )
    booking_expiry = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(days=15)
    )
    booking_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("booked", "Booked"),
            ("paid", "Paid"),
            ("cancel", "Cancelled")
        ],
        default="draft",
        required=True,
    )

    @api.depends("final_price")
    def _compute_booking_amount(self):
        for rec in self:
            rec.booking_amount = rec.final_price * 0.10

    @api.depends("final_price", "booking_amount")
    def _compute_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.final_price - rec.booking_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "estate.booking.sequence"
                    )
                    or "New"
                )
        bookings = super().create(vals_list)

        return bookings

    def action_pay_booking(self):
        self.ensure_one()
        if not self.buyer_id:
            raise UserError(
                _("No buyer is selected for this booking.")
            )

        if not self.payment_mode:
            raise UserError(
                _("Please select a payment mode.")
            )

        self.booking_state = "booked"
        self.property_id.write({
            "state": "booked",
        })

        return True

    def action_pay_remaining(self):
        self.ensure_one()

        if self.booking_state != "booked":
            raise UserError(
                _("Only booked properties can make the remaining payment.")
            )
        if not self.payment_mode:
            raise UserError(
                _("Please select a payment mode before making the remaining payment.")
            )

        payment = self.env["estate.property.payment"].create({
            "booking_id": self.id,
        })

        return {
            "type": "ir.actions.act_window",
            "name": _("Property Payment"),
            "res_model": "estate.property.payment",
            "view_mode": "form",
            "res_id": payment.id,
            "target": "current",
        }

    def action_cancel(self):
        self.ensure_one()
        self.booking_state = "cancel"
        self.property_id.state = "canceled"

        offers = self.property_id.offer_ids
        offers.status = False
        if self.property_id:
            self.property_id.write({
                "state": "offer_received",
            })

        return True
