from odoo import api, fields, models, _ , Command
from odoo.exceptions import UserError, ValidationError


class AccountCustomDutyWizard(models.TransientModel):
    _name = "account.custom.duty.wizard"
    _description = "Custom Duty Wizard"

    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    move_id = fields.Many2one("account.move", string="Bill Refrence", required=True)
    currency_id = fields.Many2one(
        "res.currency", string="Currency", default=lambda self: self.env.company.currency_id
    )
    journal_entry_number = fields.Char(string="Journal Entry Number", related="move_id.name")
    journal_entry_date = fields.Date(
        string="Journal Entry Date", default=fields.Date.context_today, readonly=True
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        readonly=True,
        default=lambda self: self.env.company.account_import_journal_id,
    )
    bill_of_entry_number = fields.Char(
        string="Bill of Entry Number", related="move_id.l10n_in_shipping_bill_number",
        readonly=False
    )
    bill_of_entry_date = fields.Date(
        string="Bill of Entry Date", related="move_id.l10n_in_shipping_bill_date",
        readonly=False
    )
    port_code_id = fields.Many2one(
        "l10n_in.port.code", string="Port Code", related="move_id.l10n_in_shipping_port_code_id",
        readonly=False
    )
    custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",
        currency_field="currency_id",
        default=1,
    )
    line_ids = fields.One2many("account.custom.duty.line", "wizard_id", string="Product Lines")
    total_custom_duty_and_additional_charges = fields.Monetary(
        string="Total Custom Duty and Additional Charges",
        currency_field="currency_id",
        compute="_compute_total_custom_duty_and_additional_charges",
    )
    total_tax_amount = fields.Monetary(
        string="Total Tax Amount",
        currency_field="currency_id",
        compute="_compute_total_tax_amount",
    )
    total_amount_payable = fields.Monetary(
        string="Total Amount Payable",
        currency_field="currency_id",
        compute="_compute_total_amount_payable",
    )
    account_import_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Default Import Custom Duty Account",
        related="company_id.account_import_custom_duty_account_id",
    )
    account_import_default_tax_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Default Import Tax Account",
        related="company_id.account_import_default_tax_account_id",
    )
    account_journal_entry_custom_duty = fields.Many2one(
        "account.move",
        string="Custom Duty Journal Entry",
        readonly=True,
        related="move_id.account_journal_entry_custom_duty",
    )

    @api.constrains("custom_currency_rate")
    def _check_positive_currency_rate(self):
        """Ensures that the custom currency rate is always greater than zero."""
        for rec in self:
            if rec.custom_currency_rate <= 0:
                raise ValidationError(_("Currency Rate must be greater than zero."))

    @api.depends("line_ids.custom_duty")
    def _compute_total_custom_duty_and_additional_charges(self):
        """Computes the total custom duty and additional charges."""
        for rec in self:
            rec.total_custom_duty_and_additional_charges = sum(rec.line_ids.mapped("custom_duty"))

    @api.depends("line_ids.tax_amount")
    def _compute_total_tax_amount(self):
        """Computes the total tax amount for the bill entry."""
        for rec in self:
            rec.total_tax_amount = sum(rec.line_ids.mapped("tax_amount"))

    @api.depends("total_custom_duty_and_additional_charges", "total_tax_amount")
    def _compute_total_amount_payable(self):
        """Computes the total amount payable for the bill entry."""
        for rec in self:
            rec.total_amount_payable = (rec.total_custom_duty_and_additional_charges + rec.total_tax_amount)

    @api.model
    def default_get(self, fields_list):
        """
        Provides default values for the wizard, primarily for bill entry lines.

        If there are no existing bill entry details for the `move_id`, it automatically creates them
        based on related `account.move.line` records.

        Context:
            - `move_id`: The account move (bill) related to this entry.

        Returns:
            dict: Default values for the wizard.
        """
        move_id = self._context.get("move_id")
        res = super().default_get(fields_list)

        if move_id:
            bill_entry_details = self.env["account.custom.duty.line"].search([("bill_id", "=", move_id)])
            if not bill_entry_details:
                move_lines = self.env["account.move.line"].search([
                    ("move_id", "=", move_id),
                    ("product_id", "!=", False),
                    ("quantity", ">", 0)
                ])
                if move_lines:
                    self.env["account.custom.duty.line"].create([
                        {
                            "bill_id": move_id,
                            "move_line_id": line.id
                        } for line in move_lines
                    ])
            res["move_id"] = move_id
            res["line_ids"] = self.env["account.custom.duty.line"].search([("bill_id", "=", move_id)])
        return res

    def action_create_and_post_journal_entry(self):
        """
        Creates and posts a journal entry for the Bill of Entry.

        - Ensures a journal entry does not already exist.
        - Validates that at least one bill entry line exists.
        - Ensures each product line has a custom duty or tax amount.
        - Creates debit and credit journal entry lines based on duty and tax amounts.
        - Posts the journal entry and links it to the account move.

        Raises:
            - `UserError`: If a journal entry already exists.
            - `UserError`: If no bill entry lines exist.
            - `UserError`: If no custom duty or tax is provided for any product line.
        """
        for record in self:
            # Check if a journal entry is already linked to the Bill of Entry
            if record.account_journal_entry_custom_duty:
                raise UserError(_("A journal entry has already been created for this Bill of Entry."))

            # Check if a journal entry already exists for the same bill reference
            existing_entry = self.env["account.move"].search([
                ("ref", "=", record.move_id.name),
                ("move_type", "=", "entry"),
                ("company_id", "=", record.company_id.id),
            ], limit=1)

            if existing_entry:
                raise UserError(_("A journal entry already exists for this Bill."))

            if not record.line_ids:
                raise UserError(_("Journal Entry can't be created without Bill Entry Line."))

            for line in record.line_ids:
                if not line.custom_duty and not line.tax_amount:
                    raise UserError(_("Please enter Custom Duty or Tax Amount for each product line."))

            journal_entry_lines = [
                Command.create({
                    "name": "Custom Duty and Additional Charges",
                    "partner_id": record.move_id.partner_id.id,
                    "debit": record.total_custom_duty_and_additional_charges,
                    "credit": 0.0,
                    "account_id": record.account_import_custom_duty_account_id.id,
                    "company_currency_id": record.currency_id.id,
                    "amount_currency": record.total_custom_duty_and_additional_charges,
                }),
                Command.create({
                    "name": "Total Payable Amount",
                    "partner_id": record.move_id.partner_id.id,
                    "debit": 0.0,
                    "credit": record.total_amount_payable,
                    "account_id": record.account_import_default_tax_account_id.id,
                    "company_currency_id": record.currency_id.id,
                    "amount_currency": -record.total_amount_payable,
                }),
            ]

            custom_duty_entries = []
            for custom_duty_line in record.line_ids:
                custom_duty_entries.append((0, 0, {
                    "move_id": record.move_id.id,
                    "move_line_id": custom_duty_line.move_line_id.id,
                    "custom_currency_rate": record.custom_currency_rate,
                    "custom_duty": custom_duty_line.custom_duty,
                    "taxable_amount": custom_duty_line.taxable_amount,
                    "tax_ids": [(6, 0, custom_duty_line.tax_ids.ids)],
                }))
                for tax in custom_duty_line.tax_ids:
                    debit_account = tax.invoice_repartition_line_ids.filtered(
                        lambda line: line.repartition_type == "tax" and line.account_id
                    ).account_id

                    if not debit_account:
                        raise UserError("No debit account found for tax")

                    tax_amount = custom_duty_line.taxable_amount * (tax.amount / 100)
                    journal_entry_lines.append(Command.create({
                        "name": f"Tax: {tax.name}",
                        "partner_id": record.move_id.partner_id.id,
                        "debit": tax_amount,
                        "credit": 0.0,
                        "account_id": debit_account.id,
                        "company_currency_id": record.currency_id.id,
                        "amount_currency": tax_amount,
                    }))

            journal_entry = self.env["account.move"].sudo().create({
                "move_type": "entry",
                "journal_id": record.journal_id.id,
                "date": record.journal_entry_date,
                "ref": record.move_id.name,
                "account_custom_currency_rate": record.custom_currency_rate,
                "account_bill_reference": record.move_id.name,
                "account_bill_entry_number": record.bill_of_entry_number,
                "account_bill_entry_date": record.bill_of_entry_date,
                "account_port_code": record.port_code_id.code,
                "line_ids": journal_entry_lines,
            })
            journal_entry.write({"custom_duty_line_ids": custom_duty_entries})

            journal_entry.action_post()
            record.move_id.account_journal_entry_custom_duty = journal_entry.id


class AccountCustomDutyLine(models.TransientModel):
    _name = "account.custom.duty.line"
    _description = "Custom Duty Line"

    bill_id = fields.Many2one("account.move", string="Bill Entry", required=True)
    wizard_id = fields.Many2one("account.custom.duty.wizard", string="Wizard Reference", ondelete="cascade")
    move_line_id = fields.Many2one("account.move.line", string="Move Line", required=True)
    product_id = fields.Many2one(
        "product.product", string="Product", related="move_line_id.product_id"
    )
    quantity = fields.Float(string="Quantity", related="move_line_id.quantity")
    unit_price = fields.Float(string="Unit Price", related="move_line_id.price_unit")
    currency_id = fields.Many2one(
        "res.currency", string="Currency", default=lambda self: self.env.company.currency_id
    )
    custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",
        currency_field="currency_id",
        related="wizard_id.custom_currency_rate",
    )
    assessable_value = fields.Monetary(
        string="Assessable Value",
        currency_field="currency_id",
        compute="_compute_assessable_value",
        store=True,
    )
    custom_duty = fields.Monetary(
        string="Custom Duty & Additional Charges", currency_field="currency_id"
    )
    taxable_amount = fields.Monetary(
        string="Taxable Amount",
        currency_field="currency_id",
        compute="_compute_taxable_amount",
        store=True,
    )
    tax_ids = fields.Many2many(
        "account.tax", string="Taxes", domain=[("type_tax_use", "=", "purchase")]
    )
    tax_amount = fields.Monetary(
        string="Tax Amount",
        currency_field="currency_id",
        compute="_compute_tax_amount",
        store=True,
        default=0.0,
    )

    @api.constrains("custom_duty", "tax_amount")
    def _check_positive_values(self):
        """Ensure that the Custom Duty and Tax Amount fields are not negative."""
        for record in self:
            if record.custom_duty < 0:
                raise ValidationError(_("Custom Duty cannot be negative."))
            if record.tax_amount < 0:
                raise ValidationError(_("Tax Amount cannot be negative."))

    @api.depends("quantity", "unit_price", "wizard_id.custom_currency_rate")
    def _compute_assessable_value(self):
        """Compute the assessable value for the custom duty calculation."""
        for record in self:
            record.assessable_value = (
                record.quantity * record.unit_price * record.wizard_id.custom_currency_rate
            )

    @api.depends("assessable_value", "custom_duty")
    def _compute_taxable_amount(self):
        """Compute the taxable amount by adding the assessable value and custom duty."""
        for record in self:
            record.taxable_amount = record.assessable_value + record.custom_duty

    @api.depends("taxable_amount", "tax_ids")
    def _compute_tax_amount(self):
        """Compute the total tax amount based on the taxable amount and tax rates."""
        for record in self:
            if record.tax_ids:
                tax_multiplier = sum(record.tax_ids.mapped("amount")) / 100
                record.tax_amount = record.taxable_amount * tax_multiplier
