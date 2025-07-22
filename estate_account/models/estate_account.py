from odoo import models, Command
from odoo.exceptions import ValidationError


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def _raise_invoice_data_missing(self):
        raise ValidationError("Please set a Buyer and Selling Price before generating an invoice.")

    def action_mark_sold(self):
        self.check_access('write')
        res = super().action_mark_sold()

        for record in self:
            if not record.buyer or not record.selling_price:
                record._raise_invoice_data_missing()

            try:
                invoice_vals = {
                    "partner_id": record.buyer.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create({
                            "name": "6% Commission",
                            "quantity": 1,
                            "price_unit": 0.06 * record.selling_price,
                        }),
                        Command.create({
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }),
                    ]
                }
                self.env["account.move"].sudo().create(invoice_vals)

            except Exception:  # noqa: BLE001
                raise ValidationError("An error occurred during invoice generation.")

        return res
