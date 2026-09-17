from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    booking_id = fields.Many2one(
        "estate.booking",
        string="Real Estate Booking",
    )

    def action_open_invoice(self):
        self.ensure_one()
        return {
            "name": "Invoice",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
