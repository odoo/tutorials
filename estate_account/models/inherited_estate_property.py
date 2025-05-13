from datetime import datetime

from odoo import models, Command


class EstateModel(models.Model):
    _inherit = "estate.property"

    # Adding a new field to store the invoice reference
    # Creates an invoice in Accounting (account.move)
    def action_set_sold(self):
        if super().action_set_sold() is True:
            for record in self:
                invoice_vals = record._prepare_invoice()

                self.env["account.move"].create(invoice_vals)

    # move_type means types of invoice
    def _prepare_invoice(self):
        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_date": datetime.today(),
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": (self.selling_price * 0.06),
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }
                ),
            ],
        }
        return invoice_vals
