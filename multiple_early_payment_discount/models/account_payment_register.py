from datetime import timedelta

from odoo import api, models, fields


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    is_manual_amount = fields.Boolean(compute="_compute_is_manual_amount")

    @api.depends('amount')
    def _compute_is_manual_amount(self):
        for wizard in self:
            wizard.is_manual_amount = bool(wizard.custom_user_amount)
            wizard._compute_payment_difference()
            if not wizard.line_ids:
                return
            residual = sum(wizard.line_ids.mapped('amount_residual'))
            total_payment = wizard.amount + wizard.payment_difference
            if total_payment > residual:
                wizard._apply_automatic_early_payment_discount()

    @api.constrains('amount', 'line_ids', 'payment_date')
    def _check_amount_not_exceed_residual(self):
        for wizard in self:
            if wizard.line_ids:
                amount_residual = sum(wizard.line_ids.mapped('amount_residual'))
                if wizard.amount > amount_residual:
                    wizard.amount = amount_residual
                    wizard._compute_payment_difference()

    @api.depends('amount', 'payment_date', 'line_ids', 'is_manual_amount')
    def _compute_payment_difference(self):
        super()._compute_payment_difference()
        for wizard in self:
            if not wizard.payment_date or not wizard.line_ids:
                continue
            if wizard.is_manual_amount:
                wizard._calculate_discount_for_manual_amount()
            else:
                wizard._apply_automatic_early_payment_discount()

    def _calculate_discount_for_manual_amount(self):
        payment_date = self.payment_date
        entered_amount = self.amount
        discount_amount = 0.0
        moves = self.line_ids.mapped('move_id')
        payment_term = moves[:1].invoice_payment_term_id
        amount_residual = sum(moves.mapped('amount_residual'))

        if not payment_term or not payment_term.discount_line_ids or amount_residual == 0:
            return

        invoice_date = moves[:1].invoice_date or moves[:1].date
        if not invoice_date:
            return

        best_discount = None
        previous_days = 0
        for d in payment_term.discount_line_ids:
            valid_until = invoice_date + timedelta(days=previous_days + d.discount_days)
            if payment_date <= valid_until:
                best_discount = d
                break
            previous_days += d.discount_days

        if not best_discount:
            return

        discount_percentage = best_discount.discount_percentage / 100.0
        total_expected_payment = entered_amount / (1 - discount_percentage)
        discount_amount = total_expected_payment - entered_amount
        self.hide_writeoff_section = True
        self.payment_difference = discount_amount
        moves.write({
            'epd_discount_amount_currency': discount_amount,
            'epd_days_left': best_discount.discount_days
        })

    def _apply_automatic_early_payment_discount(self):
        payment_date = self.payment_date
        moves = self.line_ids.mapped('move_id')
        payment_term = moves[:1].invoice_payment_term_id

        if not payment_term or not payment_term.discount_line_ids:
            return

        invoice_date = moves[:1].invoice_date or moves[:1].date
        if not invoice_date:
            return

        best_discount = None
        previous_days = 0
        for d in payment_term.discount_line_ids:
            valid_until = invoice_date + timedelta(days=previous_days + d.discount_days)
            if payment_date <= valid_until:
                best_discount = d
                break
            previous_days += d.discount_days

        if not best_discount:
            return

        discount_amount = sum(moves.mapped('amount_residual')) * (best_discount.discount_percentage / 100.0)
        self.payment_difference = discount_amount
        self.amount = sum(moves.mapped('amount_residual')) - discount_amount
        self.hide_writeoff_section = True
        moves.write({
            'epd_discount_amount_currency': discount_amount,
            'epd_days_left': best_discount.discount_days
        })

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        discount_amount = self.payment_difference

        if discount_amount <= 0:
            return payment_vals

        discount_account = self.env['account.account'].search([('code', '=', '443000')], limit=1)
        tax_account = self.env['account.account'].search([('code', '=', '251000')], limit=1)
        moves = self.line_ids.mapped('move_id')
        payment_term = moves[:1].invoice_payment_term_id

        if not discount_account or not moves or not payment_term:
            return payment_vals
        existing_discount = any(
            line.get('name') == "Early Payment Discount"
            for line in payment_vals.get('write_off_line_vals', [])
        )
        if not existing_discount:
            move_lines = self.env['account.move.line'].search([('move_id', 'in', moves.ids)])
            tax_ids = move_lines.mapped('tax_ids')
            tax_percentage = sum(tax_ids.mapped('amount')) if tax_ids else 0.0
            if payment_term.early_pay_discount_computation == 'included' and tax_percentage > 0:
                tax_amount = discount_amount * (tax_percentage / 100.0)
                discount_amount -= tax_amount
                payment_vals['write_off_line_vals'].append({
                    'name': f"Early Payment Discount ({tax_percentage}%)",
                    'account_id': tax_account.id,
                    'partner_id': self.partner_id.id,
                    'currency_id': self.currency_id.id,
                    'amount_currency': tax_amount,
                    'balance': self.currency_id._convert(tax_amount, self.company_id.currency_id, self.company_id, self.payment_date)
                })
            payment_vals['write_off_line_vals'].append({
                'name': "Early Payment Discount",
                'account_id': discount_account.id,
                'partner_id': self.partner_id.id,
                'currency_id': self.currency_id.id,
                'amount_currency': discount_amount,
                'balance': self.currency_id._convert(discount_amount, self.company_id.currency_id, self.company_id, self.payment_date)
            })
        return payment_vals
