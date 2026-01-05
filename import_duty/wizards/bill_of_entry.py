from odoo import api, fields, models
from odoo.exceptions import UserError


class CustomWizard(models.TransientModel):
    _name = "bill.of.entry"
    _description = 'Bill of Entry Wizard'

    journal_entry_line_ids = fields.One2many(
        'account.move.line',
        compute='_compute_journal_entry_lines',
        string="Journal Entry Lines",
        store=False
    )

    journal_entry_number = fields.Char(string="Journal Entry No.", compute="_compute_entry_number")
    journal_entry_date = fields.Date(string="Journal Entry Date", default=fields.Date.today())
    import_journal_id = fields.Many2one("account.journal", string="Journal", readonly=True)
    custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="currency_id", default=80)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.ref("base.INR"))
    vendor_bill_id = fields.Many2one("account.move", string="Sale Order", readonly=True)

    reference = fields.Char(string="Reference", readonly=True)
    shipping_bill_number = fields.Char(related='vendor_bill_id.l10n_in_shipping_bill_number', string="Bill of Entry No.", readonly=False)
    shipping_bill_date = fields.Date(related='vendor_bill_id.l10n_in_shipping_bill_date', string="Bill of Entry Date", readonly=False)
    port_code_id = fields.Many2one(related='vendor_bill_id.l10n_in_shipping_port_code_id', string="Port Code", readonly=False)

    entry_line_ids = fields.One2many('bill.of.entry.line', 'wizard_id', string="Entry Lines")

    total_custom_duty = fields.Monetary(string="Total Custom Duty", compute="_compute_totals", store=True)
    total_tax_amount = fields.Monetary(string="Total Tax Amount", compute="_compute_totals", store=True)
    total_amount_payable = fields.Monetary(string="Total Amount Payable", compute="_compute_totals", store=True)

    vendor_bill_confirmed = fields.Boolean(string="Bill Confirmed")
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry", compute="_compute_journal_entry")

    @api.depends('vendor_bill_id')
    def _compute_journal_entry(self):
        for wizard in self:
            if not wizard.vendor_bill_id:
                wizard.journal_entry_id = False
                continue

            journal_entry = self.env['account.move'].search([
                ('ref', '=', f'Bill of Entry for {wizard.vendor_bill_id.name}'),
                ('state', '=', 'posted')
            ], limit=1)

            wizard.journal_entry_id = journal_entry.id if journal_entry else False

    @api.onchange('journal_entry_number')
    def _compute_journal_entry_lines(self):
        for wizard in self:
            wizard.journal_entry_line_ids = wizard.journal_entry_id.line_ids if wizard.journal_entry_id else False

    @api.depends('journal_entry_id', 'import_journal_id')
    def _compute_entry_number(self):
        for wizard in self:
            if wizard.journal_entry_id:
                wizard.journal_entry_number = wizard.journal_entry_id.name
            elif wizard.import_journal_id:
                move = self.env['account.move'].new({
                    'journal_id': wizard.import_journal_id.id,
                    'date': fields.Date.context_today(wizard),
                    'move_type': 'entry',
                    'state': 'draft',
                })
                move._set_next_sequence()
                wizard.journal_entry_number = move.name or '/'
            else:
                wizard.journal_entry_number = False

    @api.depends('entry_line_ids.custom_duty', 'entry_line_ids.tax_amount')
    def _compute_totals(self):
        for wizard in self:
            total_custom = sum(line.custom_duty for line in wizard.entry_line_ids)
            total_tax = sum(line.tax_amount for line in wizard.entry_line_ids)
            wizard.total_custom_duty = total_custom
            wizard.total_tax_amount = total_tax
            wizard.total_amount_payable = total_custom + total_tax

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        company = self.env.company
        defaults["import_journal_id"] = company.import_journal_id.id
        bill_id = self.env.context.get('default_vendor_bill_id')
        if bill_id:
            bill = self.env['account.move'].browse(bill_id)
            defaults.update({
                'shipping_bill_number': bill.l10n_in_shipping_bill_number,
                'shipping_bill_date': bill.l10n_in_shipping_bill_date,
                'port_code_id': bill.l10n_in_shipping_port_code_id.id,
                'reference': bill.name,
                'vendor_bill_confirmed': bill.on_confirm,
                'journal_entry_id': bill.bill_of_entry_move_id.id,
            })
        return defaults

    @api.onchange('custom_currency_rate', 'vendor_bill_id')
    def _onchange_fill_entry_lines(self):
        if not self.vendor_bill_id or not self.custom_currency_rate:
            self.entry_line_ids = False
            return

        lines = []
        for line in self.vendor_bill_id.invoice_line_ids:
            assessable_value = line.price_unit * self.custom_currency_rate
            lines.append((0, 0, {
                "product_id": line.product_id.id,
                "assessable_value": assessable_value,
                "tax_id": line.tax_ids.ids and line.tax_ids[0].id or False,
                "currency_id": self.currency_id.id,
            }))

        self.entry_line_ids = [(5, 0, 0)] + lines

    def action_confirm(self):
        self.ensure_one()

        custom_duty_total = sum(self.entry_line_ids.mapped('custom_duty'))
        tax_total = sum(self.entry_line_ids.mapped('tax_amount'))

        if not self.entry_line_ids:
            raise UserError("You must add at least one line.")

        first_line = self.entry_line_ids[0]
        tax_repartition = first_line.tax_id.invoice_repartition_line_ids.filtered(
            lambda l: l.repartition_type == 'tax' and l.account_id
        )

        tax_account = tax_repartition[0].account_id if tax_repartition else False

        credit_account = self.env.company.import_duty_tax_account_id
        if not credit_account:
            raise UserError("Please set the 'Import Duty Payable Account' on the company.")

        line_ids = [
            (0, 0, {
                'name': 'Custom Duty',
                'account_id': self.env.company.import_duty_account_id.id,
                'debit': custom_duty_total,
                'credit': 0.0,
            }),
        ]

        if tax_account:
            line_ids.append((0, 0, {
                'name': 'IGST on Import',
                'account_id': tax_account.id,
                'debit': tax_total,
                'credit': 0.0,
            }))

        line_ids.append((0, 0, {
            'name': 'Payable for Custom Duty',
            'account_id': credit_account.id,
            'debit': 0.0,
            'credit': custom_duty_total + (tax_total if tax_account else 0.0),
        }))

        move_vals = {
            'ref': f'Bill of Entry for {self.vendor_bill_id.name}',
            'journal_id': self.import_journal_id.id,
            'date': fields.Date.today(),
            'line_ids': line_ids,
        }

        move = self.env['account.move'].create(move_vals)
        self.vendor_bill_id.write({
            'l10n_in_shipping_bill_number': self.shipping_bill_number,
            'l10n_in_shipping_bill_date': self.shipping_bill_date,
            'l10n_in_shipping_port_code_id': self.port_code_id.id,
            'bill_of_entry_move_id': move.id,
            'on_confirm': True,
        })
        move.action_post()

        return {'type': 'ir.actions.act_window_close'}

    def action_confirm_boe(self):
        self.ensure_one()

        self.vendor_bill_id.write({
            'l10n_in_shipping_bill_number': self.shipping_bill_number,
            'l10n_in_shipping_bill_date': self.shipping_bill_date,
            'l10n_in_shipping_port_code_id': self.port_code_id.id,
        })
