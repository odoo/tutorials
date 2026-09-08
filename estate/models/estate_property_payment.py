from odoo import fields, models


class EstatePropertyPayment(models.Model):
    _name = "estate.property.payment"
    _description = "Estate Property Payment Transaction"
    _order = "payment_date desc, id desc"

    booking_id = fields.Many2one(
        "estate.property.booking",
        string="Booking",
        required=True,
        ondelete="cascade",
    )
    amount = fields.Float(
        string="Amount Paid",
        required=True,
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
    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
        readonly=True,
    )
