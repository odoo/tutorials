from odoo import Command, models


class EstateBookingPayment(models.TransientModel):
    _inherit = "estate.booking.payment"

    def action_confirm(self):
        self.ensure_one()
        booking = self.booking_id

        invoice_vals = {
            "partner_id": booking.buyer_id.id,
            "move_type": "out_invoice",
            "booking_id": booking.id,
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": booking.property_id.name,
                        "quantity": 1.0,
                        "price_unit": self.amount,
                    }
                )
            ],
        }
        self.env["account.move"].create(invoice_vals)

        booking._compute_amounts_and_status()
        booking._update_booking_and_property_status()

        return {
            "type": "ir.actions.client",
            "tag": "soft_reload",
        }
