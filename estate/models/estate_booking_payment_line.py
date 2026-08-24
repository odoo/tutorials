from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstateBookingPaymentLine(models.Model):
    _name = "estate.booking.payment.line"
    _description = "Booking Payment Transaction History"
    _order = "payment_date desc, id desc"

    booking_id = fields.Many2one(
        "estate.property.booking",
        string="Booking",
        required=True,
        ondelete="cascade",
    )
    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.context_today,
        required=True,
    )
    amount = fields.Float(string="Amount Paid", required=True)
    payment_method = fields.Selection(
        selection=[
            ('cash', "Cash"),
            ('bank', "Bank Transfer"),
            ('card', "Credit/Debit Card"),
            ('upi', "UPI / Online"),
        ],
        string="Payment Method",
        default="cash",
        required=True,
    )
    transaction_ref = fields.Char(string="Transaction Ref / Chq No")
    notes = fields.Text(string="Notes")

    @api.constrains("amount")
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Payment amount must be greater than zero."))

    @api.constrains("booking_id")
    def _check_booking_state(self):
        for rec in self:
            if rec.booking_id and rec.booking_id.state in ("confirmed", "cancelled", "expired"):
                raise ValidationError(_("Cannot add or modify payment transactions on a confirmed, cancelled, or expired booking."))

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        bookings = lines.mapped("booking_id")
        bookings._check_payment_completion_and_update_status()
        return lines

    def write(self, vals):
        bookings_before = self.mapped("booking_id")
        res = super().write(vals)
        bookings_after = self.mapped("booking_id")
        (bookings_before | bookings_after)._check_payment_completion_and_update_status()
        return res

    def unlink(self):
        bookings = self.mapped("booking_id")
        res = super().unlink()
        bookings._check_payment_completion_and_update_status()
        return res
