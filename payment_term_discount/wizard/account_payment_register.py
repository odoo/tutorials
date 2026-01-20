from odoo import models, fields, api


class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'

    apply_epd_on_partial_payment = fields.Boolean(
        string="Apply Early Payment Discount",
        help="Apply early payment discount on partial payment",
        default=False)
    show_apply_epd_on_partial_payment = fields.Boolean(compute='_compute_show_apply_epd_on_partial_payment')
    early_payment_discount_on_partial_payment = fields.Monetary(compute='_compute_payment_difference_on_partial_payment')
    hide_early_payment_discount_on_partial_payment = fields.Boolean(compute='_compute_hide_early_payment_discount_on_partial_payment')

    @api.depends('amount', 'payment_date')
    def _compute_show_apply_epd_on_partial_payment(self):
        for wizard in self:
            move = wizard.line_ids.move_id
            if wizard.custom_user_amount and move._is_eligible_for_early_payment_discount(wizard.currency_id, wizard.payment_date):
                wizard.show_apply_epd_on_partial_payment = True
            else:
                wizard.show_apply_epd_on_partial_payment = False
                wizard.apply_epd_on_partial_payment = False

    @api.depends('amount', 'apply_epd_on_partial_payment', 'payment_date')
    def _compute_payment_difference_on_partial_payment(self):
        for wizard in self:
            if wizard.apply_epd_on_partial_payment and wizard.payment_date:
                discount = wizard.line_ids._get_early_payment_discount_for_payment_date(wizard.payment_date)
                discount_percentage = discount.discount_percentage if discount else 0.0
                amount_paid = (wizard.amount * 100) / (100 - discount_percentage)
                wizard.early_payment_discount_on_partial_payment = amount_paid - wizard.amount
            else:
                wizard.early_payment_discount_on_partial_payment = 0.0

    @api.depends('apply_epd_on_partial_payment')
    def _compute_hide_early_payment_discount_on_partial_payment(self):
        for wizard in self:
            if wizard.custom_user_amount and wizard.apply_epd_on_partial_payment:
                wizard.hide_early_payment_discount_on_partial_payment = True
            else:
                wizard.hide_early_payment_discount_on_partial_payment = False

    @api.depends('can_edit_wizard', 'amount', 'installments_mode', 'apply_epd_on_partial_payment', 'payment_date')
    def _compute_payment_difference(self):
        super()._compute_payment_difference()
        for wizard in self:
            if wizard.apply_epd_on_partial_payment:
                wizard.payment_difference -= wizard.early_payment_discount_on_partial_payment

    def _get_early_payment_discount_lines(self, batch_result, payment_vals, payment_difference):
        epd_aml_values_list = []
        total_amount = 0.0
        for aml in batch_result['lines']:
            epd_aml_values_list.append({
                'aml': aml,
                'amount_currency': -aml.amount_residual_currency,
                'balance': aml.currency_id._convert(-aml.amount_residual_currency, aml.company_currency_id, date=self.payment_date),
            })
            total_amount += aml.amount_currency
        open_amount_currency = payment_difference * (-1 if self.payment_type == 'outbound' else 1)
        open_balance = self.currency_id._convert(open_amount_currency, self.company_id.currency_id, self.company_id, self.payment_date)
        payment_ratio = abs((self.amount + payment_difference) / total_amount)
        early_payment_values = self.env['account.move']._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance, payment_ratio)
        for aml_values_list in early_payment_values.values():
            payment_vals['write_off_line_vals'] += aml_values_list

        return payment_vals

    def _get_writeoff_lines(self, batch_result, payment_vals):
        if self.writeoff_is_exchange_account:
            # Force the rate when computing the 'balance' only when the payment has a foreign currency.
            # If not, the rate is forced during the reconciliation to put the difference directly on the
            # exchange difference.
            if self.currency_id != self.company_currency_id:
                payment_vals['force_balance'] = sum(batch_result['lines'].mapped('amount_residual'))
        else:
            if self.payment_type == 'inbound':
                # Receive money.
                write_off_amount_currency = self.payment_difference
            else:  # if self.payment_type == 'outbound':
                # Send money.
                write_off_amount_currency = -self.payment_difference

            payment_vals['write_off_line_vals'].append({
                'name': self.writeoff_label,
                'account_id': self.writeoff_account_id.id,
                'partner_id': self.partner_id.id,
                'currency_id': self.currency_id.id,
                'amount_currency': write_off_amount_currency,
                'balance': self.currency_id._convert(write_off_amount_currency, self.company_id.currency_id, self.company_id, self.payment_date),
            })

        return payment_vals

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'memo': self.communication,
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'write_off_line_vals': [],
        }

        if self.apply_epd_on_partial_payment:
            payment_vals = self._get_early_payment_discount_lines(batch_result, payment_vals, self.early_payment_discount_on_partial_payment)
            if self.payment_difference_handling == 'reconcile':
                if not self.currency_id.is_zero(self.payment_difference):
                    payment_vals = self._get_writeoff_lines(batch_result, payment_vals)

        else:
            if self.payment_difference_handling == 'reconcile':
                if self.early_payment_discount_mode:
                    payment_vals = self._get_early_payment_discount_lines(batch_result, payment_vals, self.payment_difference)
                elif not self.currency_id.is_zero(self.payment_difference):
                    payment_vals = self._get_writeoff_lines(batch_result, payment_vals)

        return payment_vals

    def _create_payment_vals_from_batch(self, batch_result):
        batch_values = self._get_wizard_values_from_batch(batch_result)

        if batch_values['payment_type'] == 'inbound':
            partner_bank_id = self.journal_id.bank_account_id.id
        else:
            partner_bank_id = batch_result['payment_values']['partner_bank_id']

        payment_method_line = self.payment_method_line_id

        if batch_values['payment_type'] != payment_method_line.payment_type:
            payment_method_line = self.journal_id._get_available_payment_method_lines(batch_values['payment_type'])[:1]

        payment_vals = {
            'date': self.payment_date,
            'amount': batch_values['source_amount_currency'],
            'payment_type': batch_values['payment_type'],
            'partner_type': batch_values['partner_type'],
            'memo': self._get_communication(batch_result['lines']),
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'currency_id': batch_values['source_currency_id'],
            'partner_id': batch_values['partner_id'],
            'payment_method_line_id': payment_method_line.id,
            'destination_account_id': batch_result['lines'][0].account_id.id,
            'write_off_line_vals': [],
        }

        # In case it is false, we don't add it to the create vals so that
        # _compute_partner_bank_id is executed at payment creation
        if partner_bank_id:
            payment_vals['partner_bank_id'] = partner_bank_id

        total_amount_values = self._get_total_amounts_to_pay([batch_result])
        total_amount = total_amount_values['amount_by_default']
        currency = self.env['res.currency'].browse(batch_values['source_currency_id'])
        if total_amount_values['epd_applied']:
            payment_vals['amount'] = total_amount

            epd_aml_values_list = []
            for aml in batch_result['lines']:
                if aml.move_id._is_eligible_for_early_payment_discount(currency, self.payment_date):
                    epd_aml_values_list.append({
                        'aml': aml,
                        'amount_currency': -aml.amount_residual_currency,
                        'balance': currency._convert(-aml.amount_residual_currency, aml.company_currency_id, self.company_id, self.payment_date),
                    })

            open_amount_currency = (batch_values['source_amount_currency'] - total_amount) * (-1 if batch_values['payment_type'] == 'outbound' else 1)
            open_balance = currency._convert(open_amount_currency, aml.company_currency_id, self.company_id, self.payment_date)
            early_payment_values = self.env['account.move']\
                ._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance, payment_ratio=1)   # here payment_ratio is 1 because the batch payment can't be partial
            for aml_values_list in early_payment_values.values():
                payment_vals['write_off_line_vals'] += aml_values_list

        return payment_vals
