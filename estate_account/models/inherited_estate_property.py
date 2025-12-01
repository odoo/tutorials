from odoo import models, fields, Command


class EstateModel(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.check_access('write')
        for order in self:
            invoice_vals = order._prepare_invoice()
            self.env["account.move"].sudo().create(invoice_vals)

        return super().action_sold()

    def _prepare_invoice(self):
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_date": fields.Date.context_today(self),
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": (self.selling_price * 0.06) + 100,
                    }
                )
            ],
        }
        return invoice_vals
