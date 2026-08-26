from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateBookingPaymentWizard(models.TransientModel):

    _name = "estate.booking.payment.wizard"
    _description = "Register Booking Payment"

    booking_id = fields.Many2one(
        "estate.property.booking",
        string="Booking Reference",
        required=True,
        readonly=True,
        default=lambda self: self.env.context.get("active_id"),
    )
    property_id = fields.Many2one(
        "estate.property",
        related="booking_id.property_id",
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        related="booking_id.partner_id",
        readonly=True,
    )

    total_amount = fields.Float(
        string="Total Booking Value",
        related="booking_id.total_amount",
        readonly=True,
    )
    deposit_paid = fields.Float(
        string="Total Paid So Far",
        related="booking_id.deposit_paid",
        readonly=True,
    )
    min_deposit_amount = fields.Float(
        string="Min. Deposit Required (10%)",
        related="booking_id.min_deposit_amount",
        readonly=True,
    )
    remaining_amount = fields.Float(
        string="Balance Remaining",
        related="booking_id.remaining_amount",
        readonly=True,
    )
    booking_state = fields.Selection(
        related="booking_id.state",
        readonly=True,
    )
    amount = fields.Float(
        string="Payment Amount",
        required=True,
        default=lambda self: self._default_amount(),
    )
    payment_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )
    payment_method = fields.Selection(
        selection=[
            ("cash", "Cash"),
            ("bank", "Bank Transfer / NEFT / RTGS"),
            ("card", "Credit / Debit Card"),
            ("upi", "UPI / Online Payment"),
            ("cheque", "Cheque / DD"),
            ("other", "Other"),
        ],
        required=True,
        default="bank",
    )
    transaction_ref = fields.Char(
        string="Transaction Ref / Cheque No.",
        help="Bank transaction ID, cheque number, UPI reference, etc.",
    )
    notes = fields.Text(help="Optional internal notes or instructions for this payment entry.")

    amount_after_payment = fields.Float(
        string="Balance After This Payment",
        compute="_compute_amount_after_payment",
        readonly=True,
    )

    def _default_amount(self):
        booking_id = self.env.context.get("active_id")
        if not booking_id:
            return 0.0
        booking = self.env["estate.property.booking"].browse(booking_id)
        if float_is_zero(booking.deposit_paid, precision_digits=2):
            return booking.min_deposit_amount or booking.total_amount
        return booking.remaining_amount

    @api.depends("amount", "booking_id.remaining_amount")
    def _compute_amount_after_payment(self):
        for wizard in self:
            wizard.amount_after_payment = max(wizard.remaining_amount - wizard.amount, 0.0)

    @api.constrains("amount")
    def _check_amount_positive(self):
        for wizard in self:
            if float_is_zero(wizard.amount, precision_digits=2) or wizard.amount < 0:
                raise ValidationError(
                    _("Payment amount must be greater than zero. Please enter a valid amount."),
                )

    @api.constrains("amount", "booking_id")
    def _check_amount_not_exceed_balance(self):
        for wizard in self:
            if float_compare(wizard.amount, wizard.remaining_amount, precision_digits=2) > 0:
                raise ValidationError(
                    _(
                        "Payment amount (%(amount)s) cannot exceed the remaining balance (%(balance)s) "
                        "for booking %(booking)s.",
                        amount=wizard.amount,
                        balance=wizard.remaining_amount,
                        booking=wizard.booking_id.name,
                    ),
                )

    @api.constrains("payment_date")
    def _check_payment_date_not_future(self):
        today = fields.Date.context_today(self)
        for wizard in self:
            if wizard.payment_date and wizard.payment_date > today:
                raise ValidationError(
                    _("Payment date cannot be set in the future. Please use today's date or a past date."),
                )

    def action_register_payment(self):
        self.ensure_one()

        booking = self.booking_id

        if booking.state in ("confirmed", "cancelled", "expired"):
            raise UserError(
                _(
                    "Cannot register payment on a booking that is already %(state)s. "
                    "Only Draft or Pending bookings accept new payments.",
                    state=dict(booking._fields["state"].selection).get(booking.state),
                ),
            )

        if float_is_zero(booking.remaining_amount, precision_digits=2):
            raise UserError(
                _(
                    "This booking is already fully paid. "
                    "No additional payment is required for %(booking)s.",
                    booking=booking.name,
                ),
            )

        self.env["estate.booking.payment.line"].create({
            "booking_id": booking.id,
            "payment_date": self.payment_date,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "transaction_ref": self.transaction_ref or False,
            "notes": self.notes or False,
        })

        return {"type": "ir.actions.act_window_close"}
