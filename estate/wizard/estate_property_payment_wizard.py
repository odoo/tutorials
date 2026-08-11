from odoo import fields, models
from odoo.exceptions import ValidationError


class EstatePropertyPaymentWizard(models.TransientModel):
    _name = "estate.property.payment.wizard"
    _description = "Estate Property Payment Wizard"

    booking_id = fields.Many2one(
        "estate.property.booking",
        string="Booking",
        required=True,
        readonly=True,
    )
    amount = fields.Float(
        string="Payment Amount",
        required=True,
        compute="_compute_amount",
        store=True,
        readonly=False,
    )
    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.today,
        required=True,
    )
    payment_method = fields.Selection(
        [
            ("cash", "Cash"),
            ("bank_transfer", "Bank Transfer"),
            ("card", "Credit/Debit Card"),
            ("cheque", "Cheque"),
        ],
        string="Payment Method",
        default="bank_transfer",
        required=True,
    )
    notes = fields.Text(string="Notes")

    def _compute_amount(self):
        for payment in self:
            payment.amount = payment.booking_id.remaining_amount

    def action_confirm_payment(self):
        self.ensure_one()
        if self.amount <= 0:
            raise ValidationError(message="Payment amount must be greater than zero.")
        if self.booking_id and self.amount > 0:
            partner = self.booking_id.buyer_id or self.booking_id.property_id.buyer
            if not partner:
                raise ValidationError(
                    message="Please specify a buyer for the booking before confirming payment.",
                )

            invoice = self.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": partner.id,
                    "invoice_date": self.payment_date,
                    "ref": f"Payment for {self.booking_id.name}",
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": f"Booking Payment for {self.booking_id.property_id.name} ({self.booking_id.name})",
                                "quantity": 1,
                                "price_unit": self.amount,
                            },
                        ),
                    ],
                },
            )
            invoice.action_post()

            self.env["estate.property.payment"].create(
                {
                    "booking_id": self.booking_id.id,
                    "amount": self.amount,
                    "payment_date": self.payment_date,
                    "payment_method": self.payment_method,
                    "notes": self.notes,
                    "invoice_id": invoice.id,
                },
            )
        return {"type": "ir.actions.act_window_close"}
