from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateBooking(models.Model):
    _name = "estate.booking"
    _description = "Real Estate Booking"
    _rec_name = "booking_number"

    booking_number = fields.Char(
        readonly=True,
        default="New",
        copy=False,
    )
    booking_date = fields.Date(default=fields.Date.context_today, required=True)
    expiry_date = fields.Date(compute="_compute_expiry_date", store=True)
    property_id = fields.Many2one("estate.property", required=True)
    buyer_id = fields.Many2one("res.partner", required=True)
    buyer_email = fields.Char(related="buyer_id.email", readonly=True)
    seller_id = fields.Many2one("res.partner", required=True)
    seller_contact = fields.Char(
        related="seller_id.phone",
        string="Contact Number",
        readonly=True,
    )
    final_price = fields.Float(
        string="Final Property Price",
        required=True,
    )
    booking_percentage = fields.Float(
        default=10.0,
        required=True,
    )
    booking_amount = fields.Float(
        compute="_compute_amounts_and_status",
        store=True,
    )
    total_paid_amount = fields.Float(
        string="Total Paid Amount",
        default=0.0,
    )
    remaining_amount = fields.Float(
        compute="_compute_amounts_and_status",
        store=True,
    )
    booking_status = fields.Selection(
        [
            ("pending", "Pending Payment"),
            ("booked", "Booked"),
            ("completed", "Completed"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
        required=True,
    )
    payment_status = fields.Selection(
        [
            ("pending", "Pending"),
            ("booking_paid", "Booking Amount Paid"),
            ("partial", "Partial Payment"),
            ("fully_paid", "Fully Paid"),
        ],
        compute="_compute_amounts_and_status",
        store=True,
    )
    remarks = fields.Text()

    @api.depends("booking_date")
    def _compute_expiry_date(self):
        for record in self:
            if record.booking_date:
                record.expiry_date = record.booking_date + timedelta(days=10)
            else:
                record.expiry_date = False

    @api.depends("final_price", "booking_percentage", "total_paid_amount")
    def _compute_amounts_and_status(self):
        for record in self:
            record.booking_amount = record.final_price * (
                record.booking_percentage / 100.0
            )
            total_paid = record.total_paid_amount
            record.remaining_amount = record.final_price - total_paid

            if total_paid == 0:
                record.payment_status = "pending"
            elif (
                float_compare(
                    total_paid, record.booking_amount, precision_rounding=0.01
                )
                == 0
            ):
                record.payment_status = "booking_paid"
            elif (
                float_compare(total_paid, record.final_price, precision_rounding=0.01)
                >= 0
            ):
                record.payment_status = "fully_paid"
            else:
                record.payment_status = "partial"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("booking_number") or vals.get("booking_number") == "New":
                vals["booking_number"] = self.env["ir.sequence"].next_by_code(
                    "estate.booking"
                ) or _("New")
        return super().create(vals_list)

    @api.model
    def _cron_expire_bookings(self):
        today = fields.Date.today()

        expired_bookings = self.search(
            [
                ("booking_status", "=", "pending"),
                ("expiry_date", "<=", today),
            ]
        )

        for booking in expired_bookings:
            booking.write({"booking_status": "expired"})

            accepted_offer = booking.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if accepted_offer:
                accepted_offer.write({"status": "rejected"})

            booking.property_id.write(
                {
                    "state": "offer_received",
                    "selling_price": 0.0,
                    "buyer_id": False,
                }
            )

    def action_cancel(self):
        self.ensure_one()
        if self.booking_status == "completed":
            raise UserError(_("You cannot cancel a completed booking."))

        self.booking_status = "cancelled"

        accepted_offer = self.property_id.offer_ids.filtered(
            lambda o: o.status == "accepted"
        )
        if accepted_offer:
            accepted_offer.write({"status": "rejected"})

        self.property_id.write(
            {
                "state": "offer_received",
                "selling_price": 0.0,
                "buyer_id": False,
            }
        )
        return True

    def _update_booking_and_property_status(self):
        bookings_to_book = self.env["estate.booking"]
        bookings_to_complete = self.env["estate.booking"]
        properties_to_book = self.env["estate.property"]
        properties_to_sell = self.env["estate.property"]

        for record in self:
            if record.booking_status in ("cancelled", "expired"):
                continue
            total_paid = record.total_paid_amount
            booking_amt = record.booking_amount
            final_prc = record.final_price

            # If 10% paid, change property status to 'booked' and booking to 'booked'
            if (
                record.booking_status == "pending"
                and float_compare(total_paid, booking_amt, precision_rounding=0.01) >= 0
            ):
                bookings_to_book |= record
                if record.property_id.state != "booked":
                    properties_to_book |= record.property_id

            # If full price paid, change property status to 'sold' and booking to 'completed'
            if float_compare(total_paid, final_prc, precision_rounding=0.01) >= 0:
                bookings_to_complete |= record
                if record.property_id.state != "sold":
                    properties_to_sell |= record.property_id

        if bookings_to_book:
            bookings_to_book.write({"booking_status": "booked"})
        if bookings_to_complete:
            bookings_to_complete.write({"booking_status": "completed"})
        if properties_to_book:
            properties_to_book.write({"state": "booked"})
            template = self.env.ref(
                "estate.email_template_property_booked", raise_if_not_found=False
            )
            if template:
                for prop in properties_to_book:
                    template.send_mail(prop.id, force_send=True)
        if properties_to_sell:
            properties_to_sell.action_sold()

    def action_register_payment(self):
        self.ensure_one()
        default_amount = (
            self.booking_amount
            if self.booking_status == "pending"
            else self.remaining_amount
        )

        return {
            "name": _("Register Payment"),
            "type": "ir.actions.act_window",
            "res_model": "estate.booking.payment",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_booking_id": self.id,
                "default_amount": default_amount,
            },
        }
