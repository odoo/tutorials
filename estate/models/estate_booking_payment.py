from odoo import fields, models


class EstateBookingPayment(models.TransientModel):
    _name = "estate.booking.payment"
    _description = "Real Estate Booking Payment Wizard"

    booking_id = fields.Many2one(
        "estate.booking",
        string="Booking Number",
        required=True,
    )
    payment_date = fields.Date(
        default=fields.Date.context_today,
        required=True,
    )
    amount = fields.Float(
        string="Payment Amount",
        required=True,
    )
    remarks = fields.Text()

    def action_confirm(self):
        self.ensure_one()
        booking = self.booking_id
        booking.total_paid_amount += self.amount
        booking._update_booking_and_property_status()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
