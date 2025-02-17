from odoo import models, api, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        if not self.buyer_id:
            raise ValueError("❌ Cannot create invoice: No buyer assigned to this property.")

        journal = self.env['account.journal'].search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        if not journal:
            raise ValueError(f"❌ No sales journal found for company {self.env.company.name}!")

        default_income_account = self.env['account.account'].search([
            ('account_type', 'in', ['income', 'income_other']),
            ('company_ids', 'in', self.env.company.id)
        ], limit=1)
        if not default_income_account:
            raise ValueError(f"❌ No valid income account found for company {self.env.company.name}!")
        selling_price = self.selling_price
        commission_fee = selling_price * 0.06
        admin_fee = 100.00
        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': "Commission Fee (6%)",
                    'quantity': 1,
                    'price_unit': commission_fee,
                    'account_id': default_income_account.id,
                }),
                Command.create({
                    'name': "Administrative Fee",
                    'quantity': 1,
                    'price_unit': admin_fee,
                    'account_id': default_income_account.id,
                }),
            ],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        invoice.action_post()
        return res
