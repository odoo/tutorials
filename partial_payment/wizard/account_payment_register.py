from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    communication = fields.Text()
    single_payment = fields.Boolean(compute="_compute_single_payment")
    payment_lines_ids = fields.One2many(comodel_name="account.payment.lines", inverse_name="account_payment_register_id", store=True)

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('payment_lines_ids')
    def _compute_single_payment(self):
        self.single_payment = len(self.payment_lines_ids) == 1

    # -------------------------------------------------------------------------
    # LOW-LEVEL METHODS
    # -------------------------------------------------------------------------

    @api.model
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)

        # Retrieve available_line
        if 'line_ids' in fields_list:
            if self._context.get('active_model') == 'account.move':
                lines = self.env['account.move'].browse(self._context.get('active_ids', [])).line_ids
            elif self._context.get('active_model') == 'account.move.line':
                lines = self.env['account.move.line'].browse(self._context.get('active_ids', []))
            else:
                raise UserError(_(
                    "The register payment wizard should only be called on account.move or account.move.line records."
                ))

            available_lines = self.env['account.move.line']
            valid_account_types = self.env['account.payment']._get_valid_payment_account_types()
            for line in lines:

                if line.account_type not in valid_account_types:
                    continue
                if line.currency_id:
                    if line.currency_id.is_zero(line.amount_residual_currency):
                        continue
                else:
                    if line.company_currency_id.is_zero(line.amount_residual):
                        continue
                available_lines |= line

            # Store lines
            payment_lines = []
            if available_lines:
                for line in available_lines:
                    payment_lines.append((0, 0, {
                        'partner_id': line.partner_id.id,
                        'name': line.move_name,
                        'memo_id': line.move_name,
                        'invoice_date': line.invoice_date,
                        'amount_residual': line.amount_residual,
                        'balance_amount': line.amount_residual,
                        'payment_amount': line.amount_residual
                    }))
                
        res['payment_lines_ids'] = payment_lines

        return res

    # -------------------------------------------------------------------------
    # BUSINESS METHODS
    # -------------------------------------------------------------------------

    def _create_payment_vals_from_batch(self, batch_result):
        batch_values = self._get_wizard_values_from_batch(batch_result)

        if batch_values['payment_type'] == 'inbound':
            partner_bank_id = self.journal_id.bank_account_id.id
        else:
            partner_bank_id = batch_result['payment_values']['partner_bank_id']

        payment_method_line = self.payment_method_line_id

        if batch_values['payment_type'] != payment_method_line.payment_type:
            payment_method_line = self.journal_id._get_available_payment_method_lines(batch_values['payment_type'])[:1]

        # Fetch the Partial set amount.
        memo = self._get_communication(batch_result['lines'])
        payment_line = self.payment_lines_ids.search([('memo_id', '=', memo)], order='id desc', limit=1)

        payment_vals = {
            'date': self.payment_date,
            'amount': abs(payment_line.payment_amount),
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
                ._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance)
            for aml_values_list in early_payment_values.values():
                payment_vals['write_off_line_vals'] += aml_values_list

        return payment_vals

    def _create_payment_vals_from_wizard(self, batch_result):
        amount = self.amount
        if not self.single_payment:
            amount = 0
            for line in self.payment_lines_ids:
                amount += abs(line.payment_amount)
        payment_vals = {
            'date': self.payment_date,
            'amount': amount,
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

        if self.payment_difference_handling == 'reconcile':
            if self.early_payment_discount_mode:
                epd_aml_values_list = []
                for aml in batch_result['lines']:
                    if aml.move_id._is_eligible_for_early_payment_discount(self.currency_id, self.payment_date):
                        epd_aml_values_list.append({
                            'aml': aml,
                            'amount_currency': -aml.amount_residual_currency,
                            'balance': aml.currency_id._convert(-aml.amount_residual_currency, aml.company_currency_id, date=self.payment_date),
                        })

                open_amount_currency = self.payment_difference * (-1 if self.payment_type == 'outbound' else 1)
                open_balance = self.currency_id._convert(open_amount_currency, self.company_id.currency_id, self.company_id, self.payment_date)
                early_payment_values = self.env['account.move']._get_invoice_counterpart_amls_for_early_payment_discount(epd_aml_values_list, open_balance)
                for aml_values_list in early_payment_values.values():
                    payment_vals['write_off_line_vals'] += aml_values_list

            elif not self.currency_id.is_zero(self.payment_difference):

                if self.writeoff_is_exchange_account:
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
    
    def _reconcile_payments(self, to_process, edit_mode=False):
        """ Reconcile payments using the specified partial amounts per invoice. """

        domain = [
            ('parent_state', '=', 'posted'),
            ('account_type', 'in', self.env['account.payment']._get_valid_payment_account_types()),
            ('reconciled', '=', False),
        ]

        for vals in to_process:
            payment = vals['payment']
            payment_lines = payment.move_id.line_ids.filtered_domain(domain)
            invoice_line = vals['to_reconcile']
            amount_to_reconcile = vals['create_vals']['amount']  # Get the specified partial amount
            extra_context = {'forced_rate_from_register_payment': vals['rate']} if 'rate' in vals else {}

            if abs(invoice_line.amount_residual_currency) <= abs(amount_to_reconcile):
                # Fully reconcile this invoice
                (payment_lines + invoice_line).with_context(**extra_context).reconcile()
            else:
                # Partial reconciliation - create a partial reconcile entry
                self.env['account.partial.reconcile'].create({
                    'debit_move_id': invoice_line.id if invoice_line.balance > 0 else payment_lines.id,
                    'credit_move_id': payment_lines.id if invoice_line.balance > 0 else invoice_line.id,
                    'amount': amount_to_reconcile,
                    'debit_amount_currency': amount_to_reconcile if invoice_line.balance > 0 else 0.0,
                    'credit_amount_currency': amount_to_reconcile if invoice_line.balance < 0 else 0.0,
                    'company_id': payment.company_id.id,
                })

            # Link payment to reconciled journal entries
            invoice_line.move_id.matched_payment_ids += payment

    def _create_payments(self):
        self.ensure_one()
        batches = []

        for batch in self.batches:
            batch_account = self._get_batch_account(batch)
            if self.require_partner_bank_account and (not batch_account or not batch_account.allow_out_payment):
                continue
            batches.append(batch)

        if not batches:
            raise UserError(_(
                "To record payments with %(payment_method)s, the recipient bank account must be manually validated. You should go on the partner bank account in order to validate it.",
                payment_method=self.payment_method_line_id.name,
            ))

        first_batch_result = batches[0]
        edit_mode = self.can_edit_wizard and (len(first_batch_result['lines']) == 1 or self.group_payment)
        to_process_single = []
        to_process = []

        # single_payment:
        payment_vals = self._create_payment_vals_from_wizard(first_batch_result)
        to_process_values = {
            'create_vals': payment_vals,
            'to_reconcile': first_batch_result['lines'],
            'batch': first_batch_result,
        }

        # Force the rate during the reconciliation to put the difference directly on the
        # exchange difference.
        if self.writeoff_is_exchange_account and self.currency_id == self.company_currency_id:
            total_batch_residual = sum(first_batch_result['lines'].mapped('amount_residual_currency'))
            to_process_values['rate'] = abs(total_batch_residual / self.amount) if self.amount else 0.0

        to_process_single.append(to_process_values)
        
        # Don't group payments: Create one batch per move.
        lines_to_pay = self._get_total_amounts_to_pay(batches)['lines'] if self.installments_mode in ('next', 'overdue', 'before_date') else self.line_ids
        new_batches = []
        for batch_result in batches:
            for line in batch_result['lines']:
                if line not in lines_to_pay:
                    continue
                new_batches.append({
                    **batch_result,
                    'payment_values': {
                        **batch_result['payment_values'],
                        'payment_type': 'inbound' if line.balance > 0 else 'outbound'
                    },
                    'lines': line,
                })
        batches = new_batches

        for batch_result in batches:
            to_process.append({
                'create_vals': self._create_payment_vals_from_batch(batch_result),
                'to_reconcile': batch_result['lines'],
                'batch': batch_result,
            })

        if self.single_payment or self.group_payment:

            payments = self._init_payments(to_process_single, edit_mode=edit_mode)
            self._post_payments(to_process_single, edit_mode=edit_mode)

            if self.group_payment:
                for vals in to_process:
                    vals['payment'] = to_process_single[0]['payment']
                self._reconcile_payments(to_process, edit_mode=edit_mode)
            else:
                self._reconcile_payments(to_process_single, edit_mode=edit_mode)
        else:
            payments = self._init_payments(to_process, edit_mode=edit_mode)
            self._post_payments(to_process, edit_mode=edit_mode)
            self._reconcile_payments(to_process, edit_mode=edit_mode)

        return payments
