from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Real Estate Property Booking"
    _rec_name = "property_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        readonly=True,
    )
    payment_ids = fields.One2many(
        "estate.property.payment",
        "booking_id",
        string="Payments",
    )
    booking_reference = fields.Char(
        string="Booking Ref",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
)
    total_amount = fields.Float(
        string="Total Property Amount",
        store=True,
        readonly=True,
    )
    paid_amount = fields.Float(
        compute="_compute_paid_amount",
        store=True,
    )
    balance_amount = fields.Float(
        compute="_compute_balance_amount",
        store=True,
    )
    remarks = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )


    @api.depends("payment_ids.amount")
    def _compute_paid_amount(self):
        for booking in self:
            booking.paid_amount = sum(booking.payment_ids.mapped("amount"))

    @api.depends("total_amount", "paid_amount")
    def _compute_balance_amount(self):
        for booking in self:
            booking.balance_amount = (booking.total_amount - booking.paid_amount)

    def action_cancel_booking(self):
        for booking in self:
            booking.state = "cancelled"
            property = booking.property_id
            accepted_offer = property.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            )
            if accepted_offer:
                accepted_offer.status = "refused"
            pending_offers = property.offer_ids.filtered(
                lambda offer: not offer.status
            )
            property.write({
                "buyer_id": False,
                "selling_price": 0.0,
                "state": (
                    "offer_received"
                    if pending_offers
                    else "new"
                ),
            })

    def action_confirm_booking(self):
        for booking in self:
            if booking.state == "cancelled":
                raise UserError(
                    "A cancelled booking cannot be confirmed."
                )
            if booking.paid_amount < booking.total_amount:
                raise UserError(
                    "The booking cannot be confirmed until "
                    "the full amount has been paid."
                )
            if booking.paid_amount > booking.total_amount:
                raise UserError(
                    "The paid amount cannot be greater than "
                    "the total property amount."
                )
            if not booking.buyer_id.email:
                raise UserError(
                    "The buyer does not have an email address. "
                    "Please add an email address before confirming "
                    "the booking."
                )
            booking.state = "confirmed"
            booking.property_id.action_sold()
            template = self.env.ref(
                "estate.estate_property_booking_confirmation_email"
            )
            template.send_mail(
                booking.id,
                force_send=True,
                email_values={'email_to': booking.buyer_id.email},
            )
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["booking_reference"] = self.env["ir.sequence"].next_by_code("estate.property.booking")
            property_id = vals.get("property_id")
            if property_id:
                property = self.env["estate.property"].browse(property_id)
                vals["total_amount"] = property.selling_price
                vals["buyer_id"] = property.buyer_id.id
        return super().create(vals_list)
