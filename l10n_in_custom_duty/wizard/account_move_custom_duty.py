from odoo import api, Command, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMoveCustomDuty(models.TransientModel):
    _name = "account.move.custom.duty"
    _description = "Account Move Custom Duty"
        
    @api.model
    def default_get(self, fields_list):
        """ Pre-fills the wizard with values from the active bill, linking existing
        custom duty lines and creating new ones for unmatched invoice lines.
        """
        res = super().default_get(fields_list)
        
        active_id = self.env.context.get("active_id")
        if not active_id:
            return res
        
        active_bill = self.env["account.move"].browse(active_id)
        
        custom_currency_rate = active_bill.bill_of_entry_custom_currency_rate
        
        if not custom_currency_rate:
            custom_currency_rate = self.env['res.currency']._get_conversion_rate(
                from_currency=active_bill.currency_id,
                to_currency=active_bill.company_currency_id,
                company=active_bill.company_id,
                date=active_bill._get_invoice_currency_rate_date(),
            )

        res.update({
            "journal_entry_number": active_bill.bill_of_entry_id.name if active_bill.bill_of_entry_id else "",
            "currency_id": active_bill.company_id.currency_id.id,
            "custom_currency_rate": custom_currency_rate,
            "journal_id": active_bill.company_id.import_custom_duty_journal_id.id,
            "import_duty_bill_id": active_bill.id,
            "bill_of_entry_number": active_bill.l10n_in_shipping_bill_number,
            "bill_of_entry_date": active_bill.l10n_in_shipping_bill_date,
            "port_code": active_bill.l10n_in_shipping_port_code_id.id,
            "account_move_custom_duty_line_ids": [
                Command.create({ "account_move_line_id": line.id })
                for line in active_bill.invoice_line_ids
            ],
            "bill_of_entry_id": active_bill.bill_of_entry_id.id or False,
            "line_ids": [Command.set(active_bill.bill_of_entry_id.line_ids.ids)] if active_bill.bill_of_entry_id else False,
            "bill_of_entry_state": active_bill.bill_of_entry_id.state if active_bill.bill_of_entry_id else False
        })
        
        return res

    import_duty_bill_id = fields.Many2one(comodel_name="account.move", string="Reference", readonly=True)
    custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="currency_id")
    
    # journal entry details
    journal_entry_number = fields.Char(string="Journal Entry Number", readonly=True)
    journal_entry_date = fields.Date(string="Journal Entry Date", default=lambda self: fields.Date.today())
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=True)
    
    # bill of entry details
    bill_of_entry_number = fields.Char(string="Bill of Entry Number")
    bill_of_entry_date = fields.Date(string="Bill of Entry Date")
    bill_of_entry_id = fields.Many2one(related="import_duty_bill_id.bill_of_entry_id", string="Bill of Entry")
    port_code = fields.Many2one(comodel_name="l10n_in.port.code", string="Port Code")
    line_ids = fields.One2many(comodel_name="account.move.line", related="bill_of_entry_id.line_ids")
    bill_of_entry_state = fields.Selection(related="bill_of_entry_id.state")
    
    # currency
    currency_id = fields.Many2one(comodel_name="res.currency")
    
    # custom duty line details
    account_move_custom_duty_line_ids = fields.One2many(comodel_name="account.move.custom.duty.line", inverse_name="account_move_custom_duty_id", string="Custom Duty Lines")
    
    # computed fields
    total_custom_duty_with_additional_charges = fields.Monetary(string="Total Custom Duty + Additional Charges", currency_field="currency_id", compute="_compute_custom_duty_with_additional_charges")
    total_tax_amount = fields.Monetary(string="Total Tax Amount", currency_field="currency_id", compute="_compute_total_tax_amount")
    total_amount_payable = fields.Monetary(string="Total Amount Payable", currency_field="currency_id", compute="_compute_total_amount_payable")
            
    @api.depends("account_move_custom_duty_line_ids", "account_move_custom_duty_line_ids.custom_duty_with_added_charges")
    def _compute_custom_duty_with_additional_charges(self):
        for record in self:
            record.total_custom_duty_with_additional_charges = sum(record.account_move_custom_duty_line_ids.mapped("custom_duty_with_added_charges"))

    @api.depends("account_move_custom_duty_line_ids", "account_move_custom_duty_line_ids.tax_amount")
    def _compute_total_tax_amount(self):
        for record in self:
            record.total_tax_amount = sum(record.account_move_custom_duty_line_ids.mapped("tax_amount"))
    
    @api.depends("total_custom_duty_with_additional_charges", "total_tax_amount")
    def _compute_total_amount_payable(self):
        for record in self:
            record.total_amount_payable = record.total_custom_duty_with_additional_charges + record.total_tax_amount

    @api.constrains("account_move_custom_duty_line_ids")
    def _check_custom_duty_lines(self):
        for record in self:
            if not record.account_move_custom_duty_line_ids:
                raise ValidationError("At least one Custom Duty Line must be added.")

    def action_create_and_post_journal_entry(self):
        """ Creates and posts a journal entry for custom duty, linking taxes and payable duty.
        Updates the bill of entry if it exists otherwise, creates a new one.
        """
        self.ensure_one()
        
        custom_duty_account_id = self.import_duty_bill_id.company_id.import_custom_duty_account_id
        default_tax_account_id = self.import_duty_bill_id.company_id.import_default_tax_account_id
        
        if not custom_duty_account_id or not default_tax_account_id:
            raise UserError("Custom Duty Account or Default Tax Account is not set in company settings.")
        
        bill_of_entry_lines = [
            Command.create({
                "account_id": custom_duty_account_id.id,
                "debit": self.total_custom_duty_with_additional_charges
            }),
        ]
        
        for custom_duty_line in self.account_move_custom_duty_line_ids:
            taxes = custom_duty_line.tax_ids.compute_all(custom_duty_line.taxable_amount, currency=self.currency_id)
            
            for tax_res in taxes["taxes"]:
                bill_of_entry_lines.append(Command.create({
                    "account_id": tax_res["account_id"],
                    "debit": self.currency_id.round(tax_res["amount"]),
                    "name": f"Custom Duty {tax_res.get('name', '')} for {custom_duty_line.account_move_line_id.name}"
                }))

        bill_of_entry_lines.append(
            Command.create({
                "account_id": default_tax_account_id.id,
                "credit": self.total_amount_payable
            })
        )
        
        if self.bill_of_entry_id:
            self.bill_of_entry_id.write({
                "line_ids": [Command.clear()] + bill_of_entry_lines,
            })
            bill_of_entry_record = self.bill_of_entry_id
        else:                    
            bill_of_entry_record = self.env["account.move"].create({
                "move_type": "entry",
                "journal_id": self.journal_id.id,
                "ref": f"Custom duty for {self.import_duty_bill_id.name}",
                "line_ids": bill_of_entry_lines
            })
        
        bill_of_entry_record.action_post()
        
        self.import_duty_bill_id.write({
            "bill_of_entry_custom_currency_rate": self.custom_currency_rate,
            "l10n_in_shipping_bill_number": self.bill_of_entry_number,
            "l10n_in_shipping_bill_date": self.bill_of_entry_date,
            "l10n_in_shipping_port_code_id": self.port_code.id,
            "bill_of_entry_id": bill_of_entry_record.id
        })

    def action_reset_journal_to_draft(self):
        self.ensure_one()
        
        if self.bill_of_entry_id:
            self.bill_of_entry_id.button_draft()

    def action_account_move_reversal_wizard(self):
        """ Open the reversal wizard for the bill of entry journal. """
        self.ensure_one()
        
        journal_entry = self.import_duty_bill_id.bill_of_entry_id
        
        if not journal_entry:
            raise UserError("No journal entry found to reverse.")
        
        account_move_reversal_wizard = self.env["account.move.reversal"].create({
            "journal_id": self.journal_id.id,
            "date": self.journal_entry_date,
            "move_ids": [Command.link(journal_entry.id)]
        })
        
        return {
            "type": "ir.actions.act_window",
            "name": "Reverse Entry",
            "res_model": "account.move.reversal",
            "view_mode": "form",
            "res_id": account_move_reversal_wizard.id,
            "target": "new",
        }
