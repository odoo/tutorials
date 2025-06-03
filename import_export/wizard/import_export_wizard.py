from odoo import Command, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ImportWizard(models.TransientModel):
    _name = "import.export.wizard"
    _description = "Import Duty Wizard"

    # ===== HEADER INFORMATION =====
    # Company and currency context
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        help="Company for which the import duties are being recorded",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for import duty calculations",
    )

    # ===== SOURCE DOCUMENT =====
    # Reference to the vendor bill
    invoice_id = fields.Many2one(
        "account.move",
        string="Bill Reference",
        required=True,
        help="The vendor bill to which import duties and taxes will be applied",
    )
    bill_number = fields.Char(
        string="Bill of Entry Number",
        related="invoice_id.l10n_in_shipping_bill_number",
        help="Number of the shipping bill for this import",
    )
    bill_date = fields.Date(
        string="Bill Date",
        related="invoice_id.l10n_in_shipping_bill_date",
        help="Date of the shipping bill",
    )

    # ===== IMPORT DETAILS =====
    # Import-specific information
    currency_rate = fields.Monetary(
        string="Currency Rate",
        currency_field="currency_id",
        default=80,
        help="Exchange rate used for import value calculations",
    )
    port_code_id = fields.Many2one(
        "l10n_in.port.code",
        string="Port Code",
        related="invoice_id.l10n_in_shipping_port_code_id",
        help="Shipping port code for import",
    )

    # ===== PRODUCT LINES =====
    # One2many relationship to import details
    line_ids = fields.One2many(
        "import.export.details.wizard",
        "parent_wizard_id",
        string="Product Lines",
        help="List of imported products and their duty calculations",
    )

    # ===== CALCULATIONS =====
    # Computed totals
    total_duty_amount = fields.Monetary(
        string="Total Custom Duty and Additional Charges",
        currency_field="currency_id",
        compute="_compute_total_custom_duty",
        help="Sum of all customs duty amounts across all product lines",
    )
    total_tax_amount = fields.Monetary(
        string="Total Tax Amount",
        currency_field="currency_id",
        compute="_compute_total_tax_amount",
        help="Sum of all tax amounts across all product lines",
    )
    total_amount_payable = fields.Monetary(
        string="Total Amount Payable",
        currency_field="currency_id",
        compute="_compute_total_amount_payable",
        help="Total amount to be paid (duties + taxes)",
    )

    # ===== ACCOUNTING CONFIGURATION =====
    # Journal and account settings
    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        readonly=True,
        default=lambda self: self.env.company.account_imp_journal_id,
        help="Journal used for recording import duties and taxes",
    )
    duty_account_id = fields.Many2one(
        "account.account",
        string="Custom Duty Account",
        related="company_id.account_imp_duty_acct_id",
        help="Account used for recording custom duties",
    )
    tax_account_id = fields.Many2one(
        "account.account",
        string="Tax Account",
        related="company_id.account_imp_tax_acct_id",
        help="Account used for recording import taxes",
    )

    # ===== JOURNAL ENTRY REFERENCE =====
    # Link to created journal entry
    journal_entry_id = fields.Many2one(
        "account.move",
        string="Journal Entry",
        related="invoice_id.import_export_journal_entry_id",
        help="Journal entry created for import duties and taxes",
    )
    journal_entry_lines = fields.One2many(
        related="invoice_id.import_export_journal_entry_id.line_ids",
        string="Journal Items",
        help="Lines of the created journal entry",
    )

    # ===== JOURNAL ENTRY INFORMATION =====
    # Journal entry metadata
    journal_entry_number = fields.Char(
        string="Journal Entry Number",
        compute="_compute_journal_entry_number",
        store=True,
        help="Reference number of the created journal entry",
    )
    journal_entry_date = fields.Date(
        string="Journal Entry Date",
        default=fields.Date.context_today,
        readonly=True,
        help="Date when the journal entry was created",
    )

    @api.constrains("currency_rate")
    def _check_positive_currency_rate(self):
        """Ensure currency rate is positive"""
        for record in self:
            if record.currency_rate <= 0:
                raise ValidationError("Currency Rate must be greater than zero.")

    @api.depends("line_ids.customs_duty_amount")
    def _compute_total_custom_duty(self):
        """Calculate total customs duty from all line items"""
        for record in self:
            record.total_duty_amount = sum(
                record.line_ids.mapped("customs_duty_amount"),
            )

    @api.depends("line_ids.tax_amount")
    def _compute_total_tax_amount(self):
        """Calculate total tax amount from all line items"""
        for record in self:
            record.total_tax_amount = sum(record.line_ids.mapped("tax_amount"))

    @api.depends("total_duty_amount", "total_tax_amount")
    def _compute_total_amount_payable(self):
        """Calculate total amount payable (duty + tax)"""
        for record in self:
            record.total_amount_payable = (
                record.total_duty_amount + record.total_tax_amount
            )

    @api.depends("journal_entry_id")
    def _compute_journal_entry_number(self):
        """Get the journal entry name/number"""
        for record in self:
            if record.journal_entry_id:
                record.journal_entry_number = record.journal_entry_id.name
            else:
                record.journal_entry_number = False

    @api.model
    def default_get(self, fields_list):
        """Pre-populate wizard with invoice lines"""
        # Get invoice ID from context
        invoice_id = self.env.context.get("move_id")
        res = super().default_get(fields_list)

        if not invoice_id:
            return res

        # Find all product lines in the invoice
        invoice_lines = self.env["account.move.line"].search(
            [
                ("move_id", "=", invoice_id),
                ("product_id", "!=", False),
                ("quantity", ">", 0),
            ],
        )

        # Create detail wizard lines for each product line
        if invoice_lines:
            res["line_ids"] = [
                Command.create({"invoice_line_id": line.id}) for line in invoice_lines
            ]
        res["invoice_id"] = invoice_id
        return res

    def action_confirm_post_journal_entry(self):
        """Create and post the journal entry for import duties and taxes"""
        self.ensure_one()
        # Check if a journal entry already exists
        if self.journal_entry_id:
            raise UserError(
                "A journal entry already exists for Bill of Entry %s. Please check the journal entry %s."
                % (self.invoice_id.name, self.journal_entry_id.name),
            )

        # Validate line items
        if not self.line_ids:
            raise UserError(
                "Journal Entry cannot be created without product lines.",
            )

        # Check if duty or tax is entered for each line
        for line in self.line_ids:
            if not line.customs_duty_amount and not line.tax_amount:
                raise UserError(
                    "Please enter Custom Duty and Tax Amount for each product line.",
                )

        # Create the journal entry
        journal_entry = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": self.journal_id.id,
                "date": self.journal_entry_date,
                "ref": self.invoice_id.name,
                "line_ids": [
                    Command.create(
                        {
                            "name": "Custom Duty and Additional Charges",
                            "partner_id": self.invoice_id.partner_id.id,
                            "debit": self.total_duty_amount,
                            "credit": 0.0,
                            "account_id": self.duty_account_id.id,
                            "company_currency_id": self.currency_id.id,
                            "amount_currency": self.total_duty_amount,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Total Tax Amount",
                            "partner_id": self.invoice_id.partner_id.id,
                            "debit": self.total_tax_amount,
                            "credit": 0.0,
                            "account_id": self.tax_account_id.id,
                            "company_currency_id": self.currency_id.id,
                            "amount_currency": self.total_tax_amount,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Total Amount Payable",
                            "partner_id": self.invoice_id.partner_id.id,
                            "debit": 0.0,
                            "credit": self.total_amount_payable,
                            "account_id": self.invoice_id.line_ids[0].account_id.id,
                            "company_currency_id": self.currency_id.id,
                            "amount_currency": -self.total_amount_payable,
                        },
                    ),
                ],
            },
        )
        # Post the journal entry and link it to the invoice
        journal_entry.action_post()
        self.invoice_id.import_export_journal_entry_id = journal_entry.id
