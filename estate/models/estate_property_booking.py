from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Property Booking"
    _order = "id desc"

    name = fields.Char(
        string="Booking",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        domain="[('state', 'in', ['new', 'offer_received', 'offer_accepted'])]",
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    booking_date = fields.Date(
        string="Booking Date",
        required=True,
        default=fields.Date.context_today,
    )
    expiry_date = fields.Date(string="Expiry date")
    total_amount = fields.Float(string="Total Property Price", required=True)
    min_deposit_amount = fields.Float(
        string="Min Deposit Amount (10%)",
        compute="_compute_amounts",
        store=True,
        help="10% minimum deposit required for booking",
    )
    deposit_paid = fields.Float(
        string="Total Paid Amount",
        compute="_compute_amounts",
        store=True,
    )
    remaining_amount = fields.Float(
        string="Remaining Balance",
        compute="_compute_amounts",
        store=True,
    )
    payment_status = fields.Selection(
        selection=[
            ('unpaid', "Unpaid"),
            ('partial', "Partial Installment Paid"),
            ('deposit_paid', "Min Deposit Paid (10%+)"),
            ('paid', "Fully Paid (100%)"),
        ],
        string="Payment Status",
        compute="_compute_amounts",
        store=True,
        default="unpaid",
    )
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('pending', "Pending Payment"),
            ('confirmed', "Confirmed / Paid"),
            ('expired', "Expired"),
            ('cancelled', "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="draft",
    )
    payment_line_ids = fields.One2many(
        "estate.booking.payment.line",
        "booking_id",
        string="Payment Transactions",
    )
    notes = fields.Text(string="Notes")

    @api.constrains("property_id", "state")
    def _check_duplicate_active_booking(self):
        for rec in self:
            if rec.state in ("pending", "confirmed"):
                domain = [
                    ("property_id", "=", rec.property_id.id),
                    ("id", "!=", rec.id),
                    ("state", "in", ("pending", "confirmed")),
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("Active booking already exists for this property."))

    @api.onchange("property_id")
    def _onchange_property_id(self):
        if self.property_id:
            if self.property_id.buyer_id:
                self.partner_id = self.property_id.buyer_id
            if self.property_id.selling_price:
                self.total_amount = self.property_id.selling_price
            elif self.property_id.expected_price:
                self.total_amount = self.property_id.expected_price
            if not self.booking_date:
                self.booking_date = fields.Date.context_today(self)
            if self.booking_date and not self.expiry_date:
                self.expiry_date = self.booking_date + relativedelta(days=7)

    @api.onchange("booking_date")
    def _onchange_booking_date(self):
        if self.booking_date:
            self.expiry_date = self.booking_date + relativedelta(days=7)

    @api.depends("total_amount", "payment_line_ids.amount")
    def _compute_amounts(self):
        for rec in self:
            rec.min_deposit_amount = rec.total_amount * 0.10
            rec.deposit_paid = sum(rec.payment_line_ids.mapped("amount"))
            rec.remaining_amount = rec.total_amount - rec.deposit_paid

            if rec.deposit_paid >= rec.total_amount and rec.total_amount > 0:
                rec.payment_status = "paid"
                if rec.state in ("draft", "pending"):
                    rec.state = "confirmed"
                    if rec.property_id and rec.property_id.state != "sold":
                        rec.property_id.state = "sold"
            elif rec.deposit_paid >= rec.min_deposit_amount:
                rec.payment_status = "deposit_paid"
            elif rec.deposit_paid > 0:
                rec.payment_status = "partial"
            else:
                rec.payment_status = "unpaid"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("estate.property.booking") or "New"
        return super().create(vals_list)

    def action_confirm_booking(self):
        for rec in self:
            if rec.property_id.state == "booked":
                raise UserError(_("This property is already booked by another customer."))
            if rec.property_id.state in ("sold", "cancelled"):
                raise UserError(_("A sold or cancelled property cannot be booked."))
            rec.state = "pending"
            rec.property_id.state = "booked"

    def action_cancel_booking(self):
        for rec in self:
            if rec.state == "confirmed":
                raise UserError(_("This property booking cannot be cancelled because full payment is completed."))
            rec.state = "cancelled"
            if rec.property_id and rec.property_id.state in ("booked", "offer_accepted", "pending", "draft"):
                rec.property_id.write({
                    "buyer_id": False,
                    "selling_price": 0.0,
                    "state": "offer_received" if rec.property_id.offer_ids else "new",
                })

    def action_expire_booking(self):
        for rec in self:
            if rec.state in ("confirmed", "cancelled"):
                raise UserError(_("Confirmed or cancelled bookings cannot be expired."))
            rec.state = "expired"
            if rec.property_id and rec.property_id.state == "booked":
                rec.property_id.write({
                    "buyer_id": False,
                    "selling_price": 0.0,
                    "state": "offer_received" if rec.property_id.offer_ids else "new",
                })

    @api.model
    def cron_check_expired_bookings(self):
        """Cron job to automatically expire bookings whose expiry date has passed without deposit."""
        today = fields.Date.context_today(self)
        expired_bookings = self.search([
            ("state", "in", ("draft", "pending")),
            ("expiry_date", "<", today),
        ])
        for booking in expired_bookings:
            if booking.deposit_paid < booking.min_deposit_amount:
                booking.action_expire_booking()
