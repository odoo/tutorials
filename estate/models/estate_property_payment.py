from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyPayment(models.Model):
    _name = "estate.property.payment"
    _description = "Booking Payment"
    _order = "payment_date"

    booking_id = fields.Many2one(
        "estate.property.booking",
        required=True,
        ondelete="cascade",
    )
    amount = fields.Float(
        required=True,
    )
    payment_date = fields.Date(
        default=fields.Date.today,
        required=True,
    )
    payment_type = fields.Selection(
        [
            ("advance", "Advance"),
            ("installment", "Installment"),
            ("final", "Final"),
        ],
        default="installment",
    )
    remarks = fields.Text()

    @api.constrains("amount", "booking_id")
    def _check_payment_amount(self):
        for payment in self:
            paid_amount = sum(payment.booking_id.payment_ids.mapped("amount"))
            if paid_amount > payment.booking_id.total_amount:
                raise ValidationError(
                    "The total payment amount cannot be greater "
                    "than the total property amount."
                )
