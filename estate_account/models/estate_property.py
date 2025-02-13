from odoo import Command, api, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res =  super().action_sold()
        if not self.buyer_id:
            raise ValueError("A buyer must be specified before selling the property.")
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit = 1)

        if not journal:
            raise ValueError("No sales journal found.")

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
        return res
