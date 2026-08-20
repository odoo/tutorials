from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Model for Property Booking"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env._("New"),
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        related="property_id.buyer",
        string="Buyer",
        store=True,
        readonly=False,
    )
    selling_price = fields.Float(
        related="property_id.selling_price",
        string="Offered Price",
        store=True,
    )
    property_state = fields.Selection(
        related="property_id.state",
        string="Property State",
    )

    offer_id = fields.Many2one(
        "estate.property.offer",
        string="Accepted Offer",
        compute="_compute_offer_id",
        store=True,
        readonly=True,
    )

    amount = fields.Float(
        string="Booking Amount (10%)",
        compute="_compute_booking_amount",
        store=True,
    )

    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('active', "Active"),
            ('expired', "Expired"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        compute="_compute_state",
        store=True,
        readonly=False,
        default='draft',
        required=True,
        copy=False,
    )

    expired_date = fields.Date(
        compute="_compute_expired_date",
        store=True,
        readonly=False,
    )
    create_date = fields.Date(default=fields.Date.today)

    is_near_expiry = fields.Boolean(
        string="Is Near Expiry",
        compute="_compute_expiry_status",
    )
    is_expired = fields.Boolean(
        string="Is Expired",
        compute="_compute_expiry_status",
    )
    days_to_expiry = fields.Integer(
        string="Days Until Expiration",
        compute="_compute_expiry_status",
    )

    @api.constrains("property_id", "state")
    def _check_unique_active_booking(self):
        active_records = self.filtered(lambda r: r.state == "active" and r.property_id)
        if not active_records:
            return

        active_bookings = self.search(
            [
                ("property_id", "in", active_records.mapped("property_id").ids),
                ("state", "=", "active"),
            ],
        )

        for property_id in active_records.mapped("property_id"):
            if (
                len(active_bookings.filtered(lambda b: b.property_id == property_id))
                > 1
            ):
                raise ValidationError(
                    message="A property can only have one active booking at a time.",
                )

    @api.depends("expired_date", "payment_status", "total_paid", "amount")
    def _compute_state(self):
        today = fields.Date.context_today(self)
        for record in self:
            if (
                record.expired_date
                and record.expired_date < today
                and record.total_paid < record.amount
            ):
                if record.state in ("active", "draft", False):
                    record.state = "expired"
            elif (
                record.state == "expired"
                and record.expired_date
                and record.expired_date >= today
            ):
                record.state = "active"
            elif not record.state:
                record.state = "draft"

    @api.depends("expired_date", "payment_status", "total_paid", "amount")
    def _compute_expiry_status(self):
        today = fields.Date.context_today(self)
        warning_window = today + relativedelta(days=7)
        for record in self:
            if record.expired_date:
                days = (record.expired_date - today).days
                record.days_to_expiry = max(0, days)
                record.is_expired = (
                    record.expired_date < today
                    and record.total_paid < record.amount
                    and record.state != 'cancelled'
                )
                record.is_near_expiry = (
                    (today <= record.expired_date <= warning_window)
                    and record.total_paid < record.amount
                    and record.state != 'cancelled'
                )
            else:
                record.days_to_expiry = 0
                record.is_expired = False
                record.is_near_expiry = False

    payment_ids = fields.One2many(
        "estate.property.payment",
        "booking_id",
        string="Payments History",
    )
    total_paid = fields.Float(
        string="Total Paid",
        compute="_compute_payment_totals",
        store=True,
    )
    remaining_amount = fields.Float(
        string="Remaining Balance",
        compute="_compute_payment_totals",
        store=True,
    )

    payment_status = fields.Selection(
        [('unpaid', "Unpaid"), ('partially_paid', "Partially Paid"), ('paid', "Paid")],
        compute="_compute_payment_totals",
        store=True,
        default='unpaid',
    )

    @api.depends("selling_price", "amount", "payment_ids.amount")
    def _compute_payment_totals(self):
        for record in self:
            total = sum(record.payment_ids.mapped("amount"))
            record.total_paid = total
            target_amount = record.selling_price or record.amount
            record.remaining_amount = max(0.0, target_amount - total)

            if record.total_paid <= 0:
                record.payment_status = "unpaid"
            elif record.remaining_amount <= 0:
                record.payment_status = "paid"
            else:
                record.payment_status = "partially_paid"

    @api.depends("create_date")
    def _compute_expired_date(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.expired_date = create_date + relativedelta(days=30)

    @api.depends("property_id", "property_id.offer_ids.status")
    def _compute_offer_id(self):
        for record in self:
            if not record.property_id:
                record.offer_id = False
                continue
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted",
            )

            record.offer_id = accepted_offer[0].id if accepted_offer else False

    @api.depends("property_id", "property_id.selling_price")
    def _compute_booking_amount(self):
        for record in self:
            if record.property_id:
                record.amount = record.property_id.selling_price * 0.10
            else:
                record.amount = 0.0

    def action_set_active(self):
        for record in self:
            record.state = "active"
        return True

    def action_set_cancelled(self):
        for record in self:
            record.state = "cancelled"
        return True

    def action_set_draft(self):
        for record in self:
            record.state = "draft"
        return True

    def action_confirm_sale(self):
        for record in self:
            if record.payment_status != "paid":
                raise UserError(
                    message="Payment must be completely paid before confirming the sale.",
                )
            if not record.buyer_id.email:
                raise UserError(
                    message="The buyer on this booking does not have an email address set! Please update their contact card.",
                )
            if record.property_id:
                record.property_id.state = "sold"
                template = self.env.ref(
                    "estate.email_template_property_sold",
                )
                if template:
                    template.send_mail(
                        record.property_id.id,
                        force_send=True,
                        email_values={'email_to': record.buyer_id.email},
                    )
        return True

    invoice_ids = fields.Many2many(
        "account.move",
        compute="_compute_invoice_ids",
        string="Invoices",
    )
    invoices_count = fields.Integer(compute="_compute_invoice_ids")

    @api.depends("payment_ids.invoice_id")
    def _compute_invoice_ids(self):
        for record in self:
            invoices = record.payment_ids.mapped("invoice_id")
            record.invoice_ids = invoices
            record.invoices_count = len(invoices)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("estate.property.booking")
                    or "New"
                )
        return super().create(vals_list)

    def action_open_invoices(self):
        self.ensure_one()
        return {
            "name": "Invoices",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", self.invoice_ids.ids)],
        }

    def action_pay_now(self):
        self.ensure_one()
        suggested_amount = (
            (self.amount - self.total_paid)
            if self.total_paid < self.amount
            else self.remaining_amount
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Process Payment",
            "res_model": "estate.property.payment.wizard",
            "target": "new",
            "view_mode": "form",
            "context": {
                "default_booking_id": self.id,
                "default_amount": max(0.0, suggested_amount),
            },
        }
