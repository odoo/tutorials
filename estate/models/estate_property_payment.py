from odoo import fields, models, _
from odoo.exceptions import UserError


class EstatePropertyPayment(models.Model):
    _name = "estate.property.payment"
    _description = "Property Payment"

    name = fields.Char(
        string="Payment Reference",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: "New",
    )

    booking_id = fields.Many2one(
        "estate.property.booking",
        string="Booking",
        required=True,
    )

    property_id = fields.Many2one(
        related="booking_id.property_id",
        string="Property",
        store=True,
        readonly=True,
    )

    seller_id = fields.Many2one(
        related="booking_id.seller_id",
        string="Seller",
        store=True,
        readonly=True,
    )

    buyer_id = fields.Many2one(
        related="booking_id.buyer_id",
        string="Buyer",
        store=True,
        readonly=True,
    )

    booking_amount = fields.Float(
        related="booking_id.booking_amount",
        string="Booking Amount",
        readonly=True,
    )

    remaining_amount = fields.Float(
        related="booking_id.remaining_amount",
        string="Remaining Amount",
        readonly=True,
    )
    payment_mode = fields.Selection(
        [
            ("cash", "Cash"),
            ("upi", "UPI"),
            ("cheque", "Cheque"),
        ],
        string="Payment Mode",
    )

    payment_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("paid", "Paid"),
        ],
        string="Payment Status",
        default="draft",
        required=True,
    )

    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.today,
        required=True,
    )

    def action_pay(self):
        self.ensure_one()

        if self.payment_state == "paid":
            raise UserError(
                _("This payment has already been completed.")
            )

        if not self.payment_mode:
            raise UserError(
                _("Please select a payment mode.")
            )

        if not self.booking_id:
            raise UserError(
                _("No booking is associated with this payment.")
            )

        self.payment_state = "paid"
        self.booking_id.write({
            "booking_state": "paid",
        })

        self.property_id.write({
            "state": "sold",
        })

        return True
