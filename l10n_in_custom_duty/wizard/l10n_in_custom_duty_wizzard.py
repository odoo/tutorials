from odoo import api, fields, models, _ , Command
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class L10nInCustomDutyWizard(models.TransientModel):
    _name = "l10n_in.custom.duty.wizard"
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
    bill_of_entry_number = fields.Char(
        string="Bill of Entry Number", related="move_id.l10n_in_shipping_bill_number"
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        readonly=True,
        default=lambda self: self.env.company.l10n_in_import_journal_id,
    )
    bill_of_entry_date = fields.Date(
        string="Bill of Entry Date", related="move_id.l10n_in_shipping_bill_date"
    )
    custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",
        currency_field="currency_id",
        default=1,
    )
    port_code_id = fields.Many2one(
        "l10n_in.port.code", string="Port Code", related="move_id.l10n_in_shipping_port_code_id"
    )
    line_ids = fields.One2many("l10n_in.custom.duty.line", "wizard_id", string="Product Lines")

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
    l10n_in_import_custom_duty_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Default Import Custom Duty Account",
        related="company_id.l10n_in_import_custom_duty_account_id",
    )
    l10n_in_import_default_tax_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Default Import Tax Account",
        related="company_id.l10n_in_import_default_tax_account_id",
    )
    l10n_journal_entry_custom_duty = fields.Many2one(
        "account.move",
        string="Custom Duty Journal Entry",
        readonly=True,
        related="move_id.l10n_journal_entry_custom_duty",
    )

    @api.constrains("custom_currency_rate")
    def _check_positive_currency_rate(self):
        for rec in self:
            if rec.custom_currency_rate <= 0:
                raise ValidationError(_("Currency Rate must be greater than zero."))

    @api.depends("line_ids.custom_duty")
    def _compute_total_custom_duty_and_additional_charges(self):
        for rec in self:
            rec.total_custom_duty_and_additional_charges = sum(rec.line_ids.mapped("custom_duty"))

    @api.depends("line_ids.tax_amount")
    def _compute_total_tax_amount(self):
        for rec in self:
            rec.total_tax_amount = sum(rec.line_ids.mapped("tax_amount"))

    @api.depends("total_custom_duty_and_additional_charges", "total_tax_amount")
    def _compute_total_amount_payable(self):
        for rec in self:
            rec.total_amount_payable = (rec.total_custom_duty_and_additional_charges + rec.total_tax_amount)

    @api.model
    def default_get(self, fields_list):
        move_id = self._context.get("move_id")
        res = super().default_get(fields_list)

        if move_id:
            bill_entry_details = self.env["l10n_in.custom.duty.line"].search([("bill_id", "=", move_id)])
            if not bill_entry_details:
                move_lines = self.env["account.move.line"].search([
                    ("move_id", "=", move_id),
                    ("product_id", "!=", False),
                    ("quantity", ">", 0)
                ])
                if move_lines:
                    self.env["l10n_in.custom.duty.line"].create([
                        {
                            "bill_id": move_id,
                            "move_line_id": line.id
                        } for line in move_lines
                    ])
            res["move_id"] = move_id
            res["line_ids"] = self.env["l10n_in.custom.duty.line"].search([("bill_id", "=", move_id)])
        return res

    def action_create_and_post_journal_entry(self):
        for record in self:
            if record.l10n_journal_entry_custom_duty:
                raise UserError(_("A journal entry has already been created for this Bill of Entry."))
            if not record.line_ids:
                raise UserError(_("Journal Entry Can't be created without Bill Entry Line."))
            if record.line_ids:
                for line in record.line_ids:
                    if not line.custom_duty and not line.tax_amount:
                        raise UserError(_("Please enter Custom Duty or Tax Amount for each of product line."))

            journal_entry = self.env["account.move"].sudo().create({
                "move_type": "entry",
                "journal_id": record.journal_id.id,
                "date": record.journal_entry_date,
                "ref": record.move_id.name,
                "line_ids": [
                    Command.create({
                        "name": "Custom Duty and Additional Charges",
                        "partner_id": record.move_id.partner_id.id,
                        "debit": record.total_custom_duty_and_additional_charges,
                        "credit": 0.0,
                        "account_id": record.l10n_in_import_custom_duty_account_id.id,
                        "company_currency_id": record.currency_id.id,
                        "amount_currency": record.total_custom_duty_and_additional_charges,
                    }),
                    Command.create({
                        "name": "Total Tax Amount",
                        "partner_id": record.move_id.partner_id.id,
                        "debit": record.total_tax_amount,
                        "credit": 0.0,
                        "account_id": record.l10n_in_import_default_tax_account_id.id,
                        "company_currency_id": record.currency_id.id,
                        "amount_currency": record.total_tax_amount,
                    }),
                    Command.create({
                        "name": "Total Payable Amount",
                        "partner_id": record.move_id.partner_id.id,
                        "debit": 0.0,
                        "credit": record.total_amount_payable,
                        "account_id": record.move_id.line_ids[0].account_id.id,
                        "company_currency_id": record.currency_id.id,
                        "amount_currency": -record.total_amount_payable,
                    }),
                ],
            })
            # journal_entry = self.env["account.move"].sudo().create({
            #     "move_type": "entry",
            #     "journal_id": record.journal_id.id,
            #     "date": record.journal_entry_date,
            #     "ref": record.move_id.name,
            #     "line_ids": [
            #         Command.create({
            #             "name": "Custom Duty and Additional Charges",
            #             "partner_id": record.move_id.partner_id.id,
            #             "debit": record.total_custom_duty_and_additional_charges,
            #             "credit": 0.0,
            #             "account_id": record.l10n_in_import_custom_duty_account_id.id,
            #             "company_currency_id": record.currency_id.id,
            #             "amount_currency": record.total_custom_duty_and_additional_charges,
            #         }),

            #         # Create tax lines dynamically based on applied taxes
            #         *[
            #             Command.create({
            #                 "name": f"Tax: {tax.name}",
            #                 "partner_id": record.move_id.partner_id.id,
            #                 "debit": tax_line_amount,
            #                 "credit": 0.0,
            #                 "account_id": tax_repartition.account_id.id,  # Get tax account dynamically
            #                 "company_currency_id": record.currency_id.id,
            #                 "amount_currency": tax_line_amount,
            #             })
            #             for line in record.line_ids
            #             for tax in line.tax_ids
            #             for tax_repartition in tax.invoice_repartition_line_ids
            #             if tax_repartition.account_id  # Ensure there is an account assigned
            #             for tax_line_amount in [line.tax_amount / len(line.tax_ids) if line.tax_ids else 0.0]  # Split tax amount correctly
            #         ],

            #         Command.create({
            #             "name": "Total Payable Amount",
            #             "partner_id": record.move_id.partner_id.id,
            #             "debit": 0.0,
            #             "credit": record.total_amount_payable,
            #             "account_id": record.move_id.line_ids[0].account_id.id,
            #             "company_currency_id": record.currency_id.id,
            #             "amount_currency": -record.total_amount_payable,
            #         }),
            #     ],
            # })

            journal_entry.action_post()
            record.move_id.l10n_journal_entry_custom_duty = journal_entry.id
    # def action_create_and_post_journal_entry(self):
    #     for record in self:
    #         if record.l10n_journal_entry_custom_duty:
    #             raise UserError(_("A journal entry has already been created for this Bill of Entry."))
    #         if not record.line_ids:
    #             raise UserError(_("Journal Entry can't be created without Bill Entry Lines."))

    #         # Ensure each line has either a custom duty or a tax amount
    #         for line in record.line_ids:
    #             if not line.custom_duty and not line.tax_amount:
    #                 raise UserError(_("Please enter Custom Duty or Tax Amount for each product line."))

    #         # Initialize journal entry lines
    #         journal_entry_lines = [
    #             Command.create({
    #                 "name": "Custom Duty and Additional Charges",
    #                 "partner_id": record.move_id.partner_id.id,
    #                 "debit": record.total_custom_duty_and_additional_charges,
    #                 "credit": 0.0,
    #                 "account_id": record.l10n_in_import_custom_duty_account_id.id,
    #                 "company_currency_id": record.currency_id.id,
    #                 "amount_currency": record.total_custom_duty_and_additional_charges,
    #             }),
    #         ]

    #         # Process tax lines dynamically
    #         for line in record.line_ids:
    #             for tax in line.tax_ids:
    #                 # Filter only tax repartition lines that have an account assigned
    #                 tax_repartition_lines = tax.invoice_repartition_line_ids.filtered(lambda r: r.account_id and r.repartition_type == 'tax')

    #                 # If tax has valid repartition lines
    #                 if tax_repartition_lines:
    #                     # Distribute the tax amount correctly among all applicable taxes
    #                     tax_amount = line.tax_amount / len(line.tax_ids) if line.tax_ids else 0.0

    #                     for tax_repartition in tax_repartition_lines:
    #                         journal_entry_lines.append(Command.create({
    #                             "name": f"Tax: {tax.name}",
    #                             "partner_id": record.move_id.partner_id.id,
    #                             "debit": tax_amount,
    #                             "credit": 0.0,
    #                             "account_id": tax_repartition.account_id.id,  # Use correct tax account
    #                             "company_currency_id": record.currency_id.id,
    #                             "amount_currency": tax_amount,
    #                         }))

    #         # Add the payable line (credit side)
    #         journal_entry_lines.append(Command.create({
    #             "name": "Total Payable Amount",
    #             "partner_id": record.move_id.partner_id.id,
    #             "debit": 0.0,
    #             "credit": record.total_amount_payable,
    #             "account_id": record.move_id.line_ids[0].account_id.id,  # Use correct payable account
    #             "company_currency_id": record.currency_id.id,
    #             "amount_currency": -record.total_amount_payable,
    #         }))

    #         # Create the journal entry
    #         journal_entry = self.env["account.move"].sudo().create({
    #             "move_type": "entry",
    #             "journal_id": record.journal_id.id,
    #             "date": record.journal_entry_date,
    #             "ref": record.move_id.name,
    #             "line_ids": journal_entry_lines,
    #         })

    #         journal_entry.action_post()
    #         record.move_id.l10n_journal_entry_custom_duty = journal_entry.id


class L10nInCustomDutyLine(models.TransientModel):
    _name = "l10n_in.custom.duty.line"
    _description = "Custom Duty Line"

    bill_id = fields.Many2one("account.move", string="Bill Entry", required=True)
    wizard_id = fields.Many2one("l10n_in.custom.duty.wizard", string="Wizard Reference", ondelete="cascade")
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
        for record in self:
            if record.custom_duty < 0:
                raise ValidationError(_("Custom Duty cannot be negative."))
            if record.tax_amount < 0:
                raise ValidationError(_("Tax Amount cannot be negative."))

    @api.depends("quantity", "unit_price", "wizard_id.custom_currency_rate")
    def _compute_assessable_value(self):
        for record in self:
            record.assessable_value = (
                record.quantity * record.unit_price * record.wizard_id.custom_currency_rate
            )

    @api.depends("assessable_value", "custom_duty")
    def _compute_taxable_amount(self):
        for record in self:
            record.taxable_amount = record.assessable_value + record.custom_duty

    @api.depends("taxable_amount", "tax_ids")
    def _compute_tax_amount(self):
        for record in self:
            if record.tax_ids:
                tax_multiplier = sum(record.tax_ids.mapped("amount")) / 100
                record.tax_amount = record.taxable_amount * tax_multiplier
