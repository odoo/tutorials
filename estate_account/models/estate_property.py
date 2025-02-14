from odoo import Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_button(self):
        res =  super().action_sold_button()
        if not self.buyer_id:
            raise UserError("A buyer must be specified before selling the property.")
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit = 1)

        if not journal:
            raise UserError("No sales journal found.")

        commission_amount = self.selling_price * 0.06  # 6% of selling price
        admin_fees = 100.00  # Fixed fee

        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Commission (6%)",
                    "quantity": 1,
                    "price_unit": commission_amount,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": admin_fees,
                }),
            ],
        }

        invoice = self.env['account.move'].create(invoice_vals)
        print(f"Invoice {invoice.id} created for Property {self.id}")
        return res
