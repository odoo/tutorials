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
        domain="[('state', '=', 'offer_accepted')]",
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
    expiry_date = fields.Date(
        string="Expiry date",
        default=lambda self: fields.Date.context_today(self) + relativedelta(days=7),
    )
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
        active_records = self.filtered(lambda r: r.state in ("draft", "pending", "confirmed"))
        for rec in active_records:
            if rec.property_id.state not in ("offer_accepted", "booked", "sold"):
                raise ValidationError(_("Booking can only be created for a property with an accepted offer."))

        prop_ids = active_records.mapped("property_id").ids
        if prop_ids:
            booking_counts = self.env["estate.property.booking"]._read_group(
                domain=[("property_id", "in", prop_ids), ("state", "in", ("draft", "pending", "confirmed"))],
                groupby=["property_id"],
                aggregates=["__count"],
            )
            for property_rec, count in booking_counts:
                if count > 1:
                    raise ValidationError(_("An active booking already exists for property '%s'.", property_rec.display_name))

    @api.onchange("property_id")
    def _onchange_property_id(self):
        if self.property_id:
            if self.property_id.buyer_id:
                self.partner_id = self.property_id.buyer_id
            if self.property_id.selling_price:
                self.total_amount = self.property_id.selling_price
            elif self.property_id.expected_price:
                self.total_amount = self.property_id.expected_price

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
            elif rec.deposit_paid >= rec.min_deposit_amount:
                rec.payment_status = "deposit_paid"
            elif rec.deposit_paid > 0:
                rec.payment_status = "partial"
            else:
                rec.payment_status = "unpaid"

    def _check_payment_completion_and_update_status(self):
        for rec in self:
            if rec.deposit_paid >= rec.total_amount and rec.total_amount > 0:
                if rec.state in ("draft", "pending"):
                    rec.state = "confirmed"
                if rec.property_id and rec.property_id.with_context(active_test=False).state != "sold":
                    rec.property_id.write({
                        "state": "sold",
                        "active": False,
                    })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("estate.property.booking") or "New"
        return super().create(vals_list)

    def action_confirm_booking(self):
        for rec in self:
            if rec.state in ("confirmed", "cancelled", "expired"):
                raise UserError(_("This booking cannot be confirmed because it is already %s.", rec.state))
            if rec.property_id.state in ("sold", "cancelled"):
                raise UserError(_("A sold or cancelled property cannot be booked."))
            rec.state = "pending"
            rec.property_id.state = "booked"

    def _reset_associated_property(self):
        for rec in self:
            if rec.property_id:
                accepted_offers = rec.property_id.offer_ids.filtered(lambda o: o.status == "accepted")
                if accepted_offers:
                    accepted_offers.write({"status": "rejected"})
                rec.property_id.write({
                    "buyer_id": False,
                    "selling_price": 0.0,
                    "state": "offer_received" if rec.property_id.offer_ids else "new",
                })

    def action_cancel_booking(self):
        for rec in self:
            if rec.state == "confirmed":
                raise UserError(_("This property booking cannot be cancelled because full payment is completed."))
        self.write({"state": "cancelled"})
        self._reset_associated_property()

    def action_expire_booking(self):
        for rec in self:
            if rec.state in ("confirmed", "cancelled"):
                raise UserError(_("Confirmed or cancelled bookings cannot be expired."))
        self.write({"state": "expired"})
        self._reset_associated_property()

    @api.model
    def cron_check_expired_bookings(self):
        """Cron job to automatically expire bookings whose expiry date has passed without deposit."""
        today = fields.Date.context_today(self)
        expired_bookings = self.search([
            ("state", "in", ("draft", "pending")),
            ("expiry_date", "<", today),
        ])
        to_expire = expired_bookings.filtered(lambda b: b.deposit_paid < b.min_deposit_amount)
        to_expire.action_expire_booking()
