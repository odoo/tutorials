from odoo import models, fields


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    def _get_installments_data(self, payment_currency=None, payment_date=None, next_payment_date=None):
        self._set_discount_terms_for_aml(payment_date)
        installments = super()._get_installments_data(payment_currency, payment_date, next_payment_date)
        return installments

    def _set_discount_terms_for_aml(self, payment_date=None):
        for line in self:
            invoice = line.move_id
            payment_term = invoice.invoice_payment_term_id

            if not payment_date:
                line.discount_balance = 0.0
                line.discount_amount_currency = 0.0
                continue

            discount_balance = 0.0
            discount_amount_currency = 0.0
            if payment_term.early_discount and payment_term.early_payment_discount_ids:
                discount = self._get_early_payment_discount_for_payment_date(payment_date)
                discount_percentage = discount.discount_percentage / 100 if discount else 0.0
                payment_term.discount_percentage = discount.discount_percentage if discount else 0.0
                payment_term.early_pay_discount_computation = discount.early_pay_discount_computation if discount else None

                company_currency = invoice.company_id.currency_id
                currency = invoice.currency_id
                total_amount = invoice.amount_residual
                total_amount_currency = invoice.amount_residual_signed
                if payment_term.early_pay_discount_computation in ('excluded', 'mixed'):
                    discount_balance = company_currency.round(total_amount - (invoice.amount_untaxed_signed * discount_percentage))
                    discount_amount_currency = currency.round(total_amount_currency - (invoice.amount_untaxed_in_currency_signed * discount_percentage))
                else:
                    discount_balance = company_currency.round(total_amount * (1 - discount_percentage))
                    discount_amount_currency = currency.round(total_amount_currency * (1 - discount_percentage))

                if invoice.invoice_cash_rounding_id:
                    cash_rounding_difference_currency = invoice.invoice_cash_rounding_id.compute_difference(currency, discount_amount_currency)
                    if not currency.is_zero(cash_rounding_difference_currency):
                        discount_amount_currency += cash_rounding_difference_currency
                        discount_balance = company_currency.round(discount_amount_currency / (abs(total_amount_currency / total_amount) if total_amount else 0.0)) if total_amount else 0.0

            line.discount_balance = discount_balance
            line.discount_amount_currency = discount_amount_currency

    def _get_early_payment_discount_for_payment_date(self, payment_date=None):
        for line in self:
            invoice = line.move_id
            payment_term = invoice.invoice_payment_term_id

            if not payment_date:
                line.discount_balance = 0.0
                line.discount_amount_currency = 0.0
                continue

            if payment_term.early_discount and payment_term.early_payment_discount_ids:
                validity = 0
                days_from_invoice = (payment_date - (invoice.invoice_date or invoice.date or fields.Date.context_today(invoice))).days
                for discount in payment_term.early_payment_discount_ids:
                    validity += discount.discount_days
                    if days_from_invoice <= validity:
                        return discount
        return None
