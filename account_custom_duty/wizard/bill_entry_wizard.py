from odoo import api, Command, fields, models
from odoo.exceptions import UserError, ValidationError

class BillEntryWizard(models.TransientModel):
    _name = 'bill.entry.wizard'
    _description = 'Bill Entry Wizard'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    move_id = fields.Many2one('account.move', string='Bill Reference', required=True)
    
    journal_entry_number = fields.Char(string='Journal Entry Number', compute='_compute_journal_entry_number', store=True)
    journal_entry_date = fields.Date(string='Journal Entry Date', default=fields.Date.context_today, readonly=True)
    
    custom_currency_rate = fields.Monetary(string='Custom Currency Rate', currency_field='currency_id', default=80)
    bill_of_entry_number = fields.Char(string='Bill of Entry Number', related='move_id.l10n_in_shipping_bill_number')
    bill_of_entry_date = fields.Date(string='Bill of Entry Date', related='move_id.l10n_in_shipping_bill_date')
    line_ids = fields.One2many('bill.entry.details.wizard','wizard_id', string='Product Lines')
    port_code_id = fields.Many2one('l10n_in.port.code', string='Port Code', related='move_id.l10n_in_shipping_port_code_id')

    total_custom_duty_and_additional_charges = fields.Monetary(string='Total Custom Duty and Additional Charges',currency_field='currency_id',compute='_compute_total_custom_duty_and_additional_charges')
    total_tax_amount = fields.Monetary(string='Total Tax Amount',currency_field='currency_id',compute='_compute_total_tax_amount')
    total_amount_payable = fields.Monetary(string='Total Amount Payable',currency_field='currency_id',compute='_compute_total_amount_payable')

    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True, default=lambda self: self.env.company.account_import_journal_id)
    account_import_custom_duty_account_id = fields.Many2one('account.account',string="Default Import Custom Duty Account",related='company_id.account_import_custom_duty_account_id')
    account_import_tax_account_id = fields.Many2one('account.account',string="Default Import Tax Account",related='company_id.account_import_tax_account_id')

    custom_duty_journal_entry_id = fields.Many2one('account.move',string='Custom Duty Journal Entry',readonly=True,related='move_id.custom_duty_journal_entry_id')
    custom_duty_journal_entry_lines = fields.One2many(related='move_id.custom_duty_journal_entry_id.line_ids',string="Journal Items")
    
    @api.constrains('custom_currency_rate')
    def _check_positive_currency_rate(self):
        for record in self:
            if record.custom_currency_rate <= 0:
                raise ValidationError("Currency Rate must be greater than zero.")

    @api.depends('line_ids.custom_duty')
    def _compute_total_custom_duty_and_additional_charges(self):
        for record in self:
            record.total_custom_duty_and_additional_charges = sum(record.line_ids.mapped('custom_duty'))

    @api.depends('line_ids.tax_amount')
    def _compute_total_tax_amount(self):
        for record in self:
            record.total_tax_amount = sum(record.line_ids.mapped('tax_amount'))

    @api.depends('total_custom_duty_and_additional_charges', 'total_tax_amount')
    def _compute_total_amount_payable(self):
        for record in self:
            record.total_amount_payable = (record.total_custom_duty_and_additional_charges + record.total_tax_amount)

    @api.depends('custom_duty_journal_entry_id')
    def _compute_journal_entry_number(self):
        for record in self:
            if record.custom_duty_journal_entry_id:
                record.journal_entry_number = record.custom_duty_journal_entry_id.name
            else:
                record.journal_entry_number = False

    @api.model
    def default_get(self, fields_list):
        move_id = self._context.get('move_id')
        res = super().default_get(fields_list)
        
        if not move_id:
            return res
        
        move_lines = self.env['account.move.line'].search([
        ('move_id', '=', move_id),
        ('product_id', '!=', False),
        ('quantity', '>', 0)
        ])
        
        if move_lines:
            res['line_ids'] = [
                Command.create({
                    'move_line_id': line.id
                }) for line in move_lines
            ]
        res['move_id'] = move_id
        return res
        
    def action_confirm_post_journal_entry(self):
        for record in self:
            if record.custom_duty_journal_entry_id:
                raise UserError("A journal entry already exists for this Bill of Entry.")
            if record.line_ids:
                for line in record.line_ids:
                    if not line.custom_duty and not line.tax_amount:
                        raise UserError("Please enter Custom Duty and Tax Amount for each product line.")
            if not record.line_ids:
                raise UserError("Journal Entry Cannot be created without Bill Entry Detail Line.")
            
            journal_entry = self.env['account.move'].create({
                'move_type': 'entry',  
                'journal_id': record.journal_id.id,
                'date': record.journal_entry_date,
                'ref': record.move_id.name,
                'line_ids': [
                    Command.create({
                        'name': 'Custom Duty and Additional Charges',
                        'partner_id': record.move_id.partner_id.id,
                        'debit': record.total_custom_duty_and_additional_charges,
                        'credit': 0.0,
                        'account_id': record.account_import_custom_duty_account_id.id,
                        'company_currency_id': record.currency_id.id,
                        'amount_currency': record.total_custom_duty_and_additional_charges,
                    }),
                    Command.create({
                        'name': 'Total Tax Amount',
                        'partner_id': record.move_id.partner_id.id,
                        'debit': record.total_tax_amount,
                        'credit': 0.0,
                        'account_id': record.account_import_tax_account_id.id,
                        'company_currency_id': record.currency_id.id,
                        'amount_currency': record.total_tax_amount,
                    }),
                    Command.create({
                        'name': 'Total Payable Amount',
                        'partner_id': record.move_id.partner_id.id,
                        'debit': 0.0,
                        'credit': record.total_amount_payable,
                        'account_id': record.move_id.line_ids[0].account_id.id,
                        'company_currency_id': record.currency_id.id,
                        'amount_currency': -record.total_amount_payable,
                    }),
                ],
            })
            journal_entry.action_post()
            record.move_id.custom_duty_journal_entry_id = journal_entry.id

    def action_reverse_entry(self):
        self.ensure_one()
        
        reversal_wizard = self.env['account.move.reversal'].create({
            'move_ids' : [(6, 0, [self.custom_duty_journal_entry_id.id])],
            'date' : fields.Date.context_today(self),
            'company_id' : self.company_id.id,
            'journal_id' : self.journal_id.id,
        })
        
        return {
            'name': 'Reverse Entry',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.reversal',
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_account_move_reversal').id,
            'target': 'new',
            'res_id' : reversal_wizard.id
        }

    def button_draft_journal_entry(self):
        for record in self:
            if record.custom_duty_journal_entry_id:
                record.custom_duty_journal_entry_id.button_draft()
                record.move_id.custom_duty_journal_entry_id = False
