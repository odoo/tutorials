from odoo import models, fields


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _get_total_amounts_to_pay(self, batch_results):
        res = super()._get_total_amounts_to_pay(batch_results)
        amount_by_default = res.get("amount_by_default")
        lines = res.get("lines")
        invoices = lines.mapped("move_id")
        for invoice in invoices:
            total_amount = invoice.amount_residual
            payment_term = invoice.invoice_payment_term_id
            today = fields.Date.today()
            invoice_date = invoice.invoice_date
            due_days = (today - invoice_date).days
            current_discount_days = payment_term.discount_days
            if due_days > current_discount_days:
                for discount in payment_term.early_discount_ids:
                    if due_days <= current_discount_days + discount.discount_days:
                        discount_amount = (total_amount * discount.discount_percentage) / 100
                        new_amount = total_amount - discount_amount
                        amount_by_default -= total_amount
                        amount_by_default += new_amount
                        res["epd_applied"] = True
                        break

                    current_discount_days = current_discount_days + discount.discount_days
        res["amount_by_default"] = amount_by_default
        return res
