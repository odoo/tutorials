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
