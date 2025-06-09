from odoo import api, fields, models
from odoo.exceptions import UserError


class BillOfEntryWizard(models.TransientModel):
    _name = "bill.of.entry.wizard"
    _description = "Bill of Entry Wizard"

    journal_entry_no = fields.Char(string="Journal Entry No", readonly=True)
    bill_of_entry_no = fields.Char(string="Bill of Entry No", store=True)
    reference = fields.Char(string="Reference")
    bill_of_entry_confirmed = fields.Boolean(string="Bill of Entry Confirmed", default=False)
    bill_of_entry_date = fields.Date(string="Bill of Entry Date")
    journal_entry_date = fields.Date(string="Journal Entry Date", default=fields.Date.today, readonly=True)
    move_id = fields.Many2one("account.move", string="Vendor Bill", required=True)
    journal_id = fields.Many2one("account.journal", string="Journal", readonly=True)
    company_currency_id = fields.Many2one("res.currency", string="Company Currency", default=lambda self: self.env.company.currency_id.id, readonly=True,)
    port_code = fields.Many2one("l10n_in.port.code", string="Port Code")
    journal_move_id = fields.Many2one("account.move", string="Journal entry", readonly=True)
    tax_id = fields.Many2one("account.tax", string="Tax", domain=[("type_tax_use", "=", "purchase")],)
    line_ids = fields.One2many("bill.of.entry.line.wizard", "wizard_id", string="Bill of Entry Details")
    bill_of_entry_line_ids = fields.One2many("bill.of.entry.line.wizard", "wizard_id", string="Bill of Entry Lines",)

    # monetary fields
    custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="company_currency_id", default=1.0, store=True,)
    total_cd_all = fields.Monetary(string="Total Custom Duty + Additional Charges", compute="_compute_total_cd_all", store=True, currency_field="company_currency_id",)
    total_tax_all = fields.Monetary(string="Total Tax Amount", compute="_compute_total_tax_all", store=True, currency_field="company_currency_id",)
    total_amount_all = fields.Monetary(string="Total Amount Payable", compute="_compute_total_amount_all", store=True, currency_field="company_currency_id",)

    @api.depends("line_ids.custom_duty")
    def _compute_total_cd_all(self):
        """Computes the sum of Custom Duty from all product lines."""
        for record in self:
            record.total_cd_all = sum(line.custom_duty for line in record.line_ids)

    @api.depends("line_ids.tax_amount")
    def _compute_total_tax_all(self):
        """Computes the sum of Tax Amount from all product lines."""
        for record in self:
            # breakpoint()
            record.total_tax_all = sum(line.tax_amount for line in record.line_ids)

    @api.depends("total_cd_all", "total_tax_all")
    def _compute_total_amount_all(self):
        """Computes the sum of Total Custom Duty + Total Tax Amount."""
        for record in self:
            record.total_amount_all = record.total_cd_all + record.total_tax_all


    @api.model
    def default_get(self, fields_list):
        """Set default values when opening the wizard and copy bill lines."""
        defaults = super().default_get(fields_list)
        move_id = self.env.context.get("default_move_id")
        company = self.env.company

        # Fetched required accounts from company settings
        default_journal = company.l10n_in_import_journal_id
        custom_currency_rate = company.currency_id.rate

        default_tax = self.env["account.tax"].search(
            [("type_tax_use", "=", "purchase")], limit=1
        )
        if move_id:
            move = self.env["account.move"].browse(move_id)

            defaults.update(
                {
                    "move_id": move.id,
                    "bill_of_entry_no": move.l10n_in_shipping_bill_number,
                    "bill_of_entry_date": move.l10n_in_shipping_bill_date,
                    "port_code": move.l10n_in_shipping_port_code_id.id,
                    "journal_id": default_journal.id if default_journal else False,
                    "custom_currency_rate": custom_currency_rate,
                    "tax_id": default_tax.id if default_tax else False,
                }
            )
            line_values = []
            for line in move.invoice_line_ids:
                line_values.append(
                    fields.Command.create(
                        {
                            "product_id": line.product_id.id,
                            "price_unit_foreign": line.price_unit,
                            "quantity": line.quantity,
                        }
                    )
                )
            defaults["line_ids"] = line_values

        return defaults


    def action_confirm(self):
        company = self.env.company
        journal = company.l10n_in_import_journal_id
        custom_duty_account = company.l10n_in_import_custom_duty_account_id
        tax_account = company.l10n_in_import_default_tax_account_id
        payable_account = company.l10n_in_import_custom_duty_tax_payable_account_id

        if not all(
            [
                journal,
                custom_duty_account,
                tax_account,
                payable_account,
            ]
        ):
            raise UserError("Please configure Import Journal and Accounts in settings.")

        total_custom_duty = self.total_cd_all
        total_tax_amount = self.total_tax_all
        total_amount_payable = self.total_amount_all

        move_vals = {
            "journal_id": journal.id,
            "date": fields.Date.context_today(self),
            "ref": self.reference,
            "bill_of_entry_no": self.bill_of_entry_no,
            "bill_of_entry_date": self.bill_of_entry_date,
            "port_code": self.port_code.id,
            "custom_currency_rate": self.custom_currency_rate,
            "total_cd_all": total_custom_duty,
            "total_tax_all": total_tax_amount,
            "total_amount_all": total_amount_payable,
            "line_ids": [],
        }
        move = self.env["account.move"].create(move_vals)

        entry_lines = []
        for line in self.bill_of_entry_line_ids:
            entry_lines.append(
                (0, 0, {
                    "product_id": line.product_id.id,
                    "assessable_value": line.assessable_value,
                    "custom_duty": line.custom_duty,
                    "taxable_amount": line.taxable_amount,
                    "tax_id": line.tax_id.id,
                    "tax_amount": line.tax_amount,
                    "move_id": move.id,
                })
            )

        move.write({"bill_of_entry_line_ids": entry_lines})

        move_lines = [
            # Debit: Custom Duty Account
            (
                0,
                0,
                {
                    "account_id": custom_duty_account.id,
                    "debit": total_custom_duty,
                    "credit": 0.0,
                    "move_id": move.id,
                    "name": "Custom Duty",
                },
            ),
            # Debit: IGST on Import
            (
                0,
                0,
                {
                    "account_id": tax_account.id,
                    "debit": total_tax_amount,
                    "credit": 0.0,
                    "move_id": move.id,
                    "name": "IGST on Import",
                },
            ),
            # Credit: Custom Duty Tax Payable Account
            (
                0,
                0,
                {
                    "account_id": payable_account.id,
                    "debit": 0.0,
                    "credit": total_amount_payable,
                    "move_id": move.id,
                    "name": "Custom Duty Payable",
                },
            ),
        ]

        move.write({"line_ids": move_lines})
        move.action_post()
        self.journal_move_id = move
        self.journal_entry_no = move.name
        self.move_id.journal_move_id = move

        return {"type": "ir.actions.act_window_close"}
