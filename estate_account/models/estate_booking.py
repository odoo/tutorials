from odoo import api, fields, models
from odoo.tools import float_compare


class EstateBooking(models.Model):
    _inherit = "estate.booking"

    invoice_ids = fields.One2many(
        "account.move",
        "booking_id",
        string="Invoices",
        domain=[("move_type", "=", "out_invoice")],
    )
    total_paid_amount = fields.Float(
        compute="_compute_amounts_and_status",
        store=True,
    )

    @api.depends(
        "final_price",
        "booking_percentage",
        "invoice_ids.amount_total",
        "invoice_ids.amount_residual",
        "invoice_ids.payment_state",
    )
    def _compute_amounts_and_status(self):
        super()._compute_amounts_and_status()

        for record in self:
            posted_invoices = record.invoice_ids.filtered(lambda m: m.state == "posted")
            total_paid = sum(
                posted_invoices.mapped(lambda m: m.amount_total - m.amount_residual)
            )
            record.total_paid_amount = total_paid
            record.remaining_amount = record.final_price - total_paid

            if total_paid == 0:
                record.payment_status = "pending"
            elif (
                float_compare(total_paid, record.final_price, precision_rounding=0.01)
                >= 0
            ):
                record.payment_status = "fully_paid"
            elif (
                float_compare(
                    total_paid, record.booking_amount, precision_rounding=0.01
                )
                == 0
            ):
                record.payment_status = "booking_paid"
            else:
                record.payment_status = "partial"

        self._update_booking_and_property_status()
