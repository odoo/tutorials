from datetime import datetime
from odoo import models, Command, api, _
from odoo.exceptions import AccessError, UserError


class EstateModel(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.check_access("write")
        if super().action_sold() is True:
            invoice_vals = self._prepare_invoice()
            self.env["account.move"].sudo().create(invoice_vals)


    def _prepare_invoice(self):
        """Prepare invoice vals with strict field control"""
        return {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_date": datetime.today(),
            "invoice_line_ids": [
                Command.create({
                    "name": f"Commission for {self.name}",
                    "quantity": 1,
                    "price_unit": (self.selling_price * 0.06),  # 6% commission
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,  # Fixed fee
                }),
            ],
        }
