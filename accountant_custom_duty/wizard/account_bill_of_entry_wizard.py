from odoo import api, fields, models


class CustomWizard(models.TransientModel):
    _name = "account.bill.of.entry.wizard"
    _description = "Custom Wizard"

    l10n_in_journal_entry_date = fields.Date(string="Journal Entry Date", default=fields.Date.today())
    l10n_in_custom_duty_import_journal_id = fields.Many2one("account.journal", string="Journal")
    l10n_in_account_custom_duty_income_id = fields.Many2one(comodel_name="account.account", string="Separate account for income discount")

    l10n_in_import_default_tax_account = fields.Many2one("account.account", string="Journal Suspense Account", check_company=True)
    l10n_in_custom_duty_tax_payable_account = fields.Many2one("account.account", string="Custom Duty Tax Payable Account", check_company=True)

    l10n_in_company_currency_id = fields.Many2one("res.currency", string="Company Currency ID", default=lambda self: self.env.ref("base.INR"))
    l10n_in_custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="l10n_in_company_currency_id", default=1.0)

    l10n_in_reference = fields.Char(string="Bill Number", help="Bill No. on which this model is accessed", readonly=True)
    l10n_in_journal_entry_number = fields.Char(string="Journal Entry Number", compute="_compute_l10n_in_journal_entry_number", store=True)

    l10n_in_shipping_bill_number = fields.Char("Bill of Entry No.")
    l10n_in_shipping_bill_date = fields.Date("Bill of Entry Date")
    l10n_in_shipping_port_code_id = fields.Many2one("l10n_in.port.code", "Port code")
    
    l10n_in_move_line_ids = fields.One2many("account.move.line.wizard", "wizard_id", string="Product Lines")

    l10n_in_total_custom_duty = fields.Monetary(string="Total Custom Duty + Additional Charges", compute="_compute_l10n_in_total_custom_duty", store=True, currency_field="l10n_in_company_currency_id")

    l10n_in_total_l10n_in_tax_amount = fields.Monetary(string="Total Tax Amount", compute="_compute_l10n_in_total_l10n_in_tax_amount", store=True, currency_field="l10n_in_company_currency_id")

    l10n_in_total_amount_payable = fields.Monetary(string="Total Amount Payable", compute="_compute_l10n_in_total_amount_payable", store=True, currency_field="l10n_in_company_currency_id")
    l10n_in_journal_item_ids = fields.One2many("account.move.line.wizard", "wizard_id", compute="_compute_journal_items", string="Journal Items")
    move_id = fields.Many2one("account.move", string="Journal Entry", required=True)

    @api.depends("l10n_in_custom_duty_import_journal_id")
    def _compute_l10n_in_journal_entry_number(self):
        """Compute the next journal entry number based on the selected journal."""
        for wizard in self:
            if wizard.l10n_in_custom_duty_import_journal_id:
                wizard.l10n_in_journal_entry_number = wizard._get_next_sequence(wizard.l10n_in_custom_duty_import_journal_id)

    def _get_next_sequence(self, journal):
        """Fetch the next sequence number for the provided journal."""
        last_move = self.env["account.move"].search([("journal_id", "=", journal.id)], order="name desc", limit=1)
        last_sequence = last_move.name if last_move else None

        today = fields.Date.today()
        fy_start = today.year if today.month >= 4 else today.year - 1
        fy_end = fy_start + 1
        fy_format = f"{str(fy_end)}/{today.month:02d}"

        if last_sequence and last_sequence.split("/")[2] == f"{today.month:02d}":
            parts = last_sequence.split("/")
            last_number = int(parts[-1])
            new_number = str(last_number + 1).zfill(4)
            parts[-1] = new_number
            return "/".join(parts)
        else:
            return f"{journal.code}/{fy_format}/0001"

    @api.depends("l10n_in_total_custom_duty", "l10n_in_total_l10n_in_tax_amount", "l10n_in_total_amount_payable")
    def _compute_journal_items(self):
        for wizard in self:
            journal_items = [
                (0,0,
                    {
                        "account_id": wizard.env.company.l10n_in_account_custom_duty_income_id.id,
                        "label": "Custom Duty Account",
                        "debit": wizard.l10n_in_total_custom_duty,
                        "credit": 0.0,
                    },
                ),
                (0,0,
                    {
                        "account_id": wizard.env.company.l10n_in_import_default_tax_account.id,
                        "label": "IGST on Import Account",
                        "debit": wizard.l10n_in_total_l10n_in_tax_amount,
                        "credit": 0.0,
                    },
                ),
                (0,0,
                    {
                        "account_id": wizard.env.company.l10n_in_custom_duty_tax_payable_account.id,
                        "label": "Custom Duty Tax Payable Account",
                        "debit": 0.0,
                        "credit": wizard.l10n_in_total_amount_payable,
                    },
                ),
            ]
            wizard.l10n_in_journal_item_ids = journal_items

    @api.depends("l10n_in_move_line_ids.l10n_in_custom_duty_additional")
    def _compute_l10n_in_total_custom_duty(self):
        for wizard in self:
            wizard.l10n_in_total_custom_duty = sum(
                wizard.l10n_in_move_line_ids.mapped("l10n_in_custom_duty_additional")
            )

    @api.depends("l10n_in_move_line_ids.l10n_in_tax_amount")
    def _compute_l10n_in_total_l10n_in_tax_amount(self):
        for wizard in self:
            wizard.l10n_in_total_l10n_in_tax_amount = sum(
                wizard.l10n_in_move_line_ids.mapped("l10n_in_tax_amount")
            )

    @api.depends("l10n_in_move_line_ids.l10n_in_custom_duty_additional", "l10n_in_move_line_ids.l10n_in_tax_amount")
    def _compute_l10n_in_total_amount_payable(self):
        for wizard in self:
            wizard.l10n_in_total_amount_payable = (wizard.l10n_in_total_custom_duty + wizard.l10n_in_total_l10n_in_tax_amount)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        company = self.env.company
        defaults["l10n_in_custom_duty_import_journal_id"] = (company.l10n_in_custom_duty_import_journal_id.id)
        defaults["l10n_in_account_custom_duty_income_id"] = (company.l10n_in_account_custom_duty_income_id.id)
        defaults["l10n_in_import_default_tax_account"] = (company.l10n_in_import_default_tax_account.id)
        defaults["l10n_in_custom_duty_tax_payable_account"] = (company.l10n_in_custom_duty_tax_payable_account.id)

        move_id = self._context.get("default_move_id")
        if move_id:
            move = self.env["account.move"].browse(move_id)
            lines = []
            defaults["l10n_in_shipping_port_code_id"] = (
                move.l10n_in_shipping_port_code_id.id
            )
            for line in move.invoice_line_ids:
                lines.append(
                    (0,0,
                        {
                            "wizard_id": self.id,
                            "product_id": line.product_id.id,
                            "name": line.name,
                            "quantity": line.quantity,
                            "price_unit": line.price_unit,
                            "account_id": line.account_id.id,
                            "tax_ids": [(6, 0, line.tax_ids.ids)],
                            "l10n_in_assessable_value": line.l10n_in_assessable_value,
                            "l10n_in_custom_duty_additional": line.l10n_in_custom_duty_additional,
                            "l10n_in_taxable_amount": line.l10n_in_taxable_amount,
                            "l10n_in_tax_amount": line.l10n_in_tax_amount,
                        },
                    )
                )

            defaults["l10n_in_move_line_ids"] = lines

        return defaults

    def action_confirm(self):
        move_vals = {
            "date": self.l10n_in_journal_entry_date,
            "journal_id": self.l10n_in_custom_duty_import_journal_id.id,
            "l10n_in_custom_currency_rate": self.l10n_in_custom_currency_rate,
            "l10n_in_total_custom_duty": self.l10n_in_total_custom_duty,
            "l10n_in_total_l10n_in_tax_amount": self.l10n_in_total_l10n_in_tax_amount,
            "l10n_in_total_amount_payable": self.l10n_in_total_amount_payable,
            "l10n_in_shipping_bill_number": self.l10n_in_shipping_bill_number,
            "l10n_in_shipping_bill_date": self.l10n_in_shipping_bill_date,
            "l10n_in_shipping_port_code_id": self.l10n_in_shipping_port_code_id.id,
            "line_ids": []
        }

        move = self.env["account.move"].create(move_vals)

        line_ids = []
        for line in self.l10n_in_journal_item_ids:
            line_ids.append(
                (0,0,
                    {
                        "account_id": line.account_id.id,
                        "name": line.label,
                        "debit": line.debit,
                        "credit": line.credit,
                    },
                )
            )
        move.write({"line_ids": line_ids, "company_currency_id": self.l10n_in_company_currency_id.id})

        bill_of_entry_line_ids = []
        for line in self.l10n_in_move_line_ids:
            bill_of_entry_line_ids.append(
               (0,0,
                {
                    "account_id": line.account_id.id,
                    "name": line.label or "Bill Entry",
                    "product_id": line.product_id.id or False,
                    "quantity": line.quantity or 1.0,
                    "price_unit": line.price_unit * self.l10n_in_custom_currency_rate,
                    "tax_ids": [(6, 0, line.tax_ids.ids)] if line.tax_ids else [],
                    "l10n_in_assessable_value": line.l10n_in_assessable_value,
                    "l10n_in_custom_duty_additional": line.l10n_in_custom_duty_additional,
                    "l10n_in_taxable_amount": line.l10n_in_taxable_amount,
                    "l10n_in_tax_amount": line.l10n_in_tax_amount,
                })
            )
        move.write({"bill_of_entry_line_ids": bill_of_entry_line_ids})
            

        self.move_id.write(
            {
                "l10n_in_journal_entry_number": self.l10n_in_journal_entry_number,
            }
        )
        move.action_post()
        self.move_id.is_confirmed = True
        return {"type": "ir.actions.act_window_close"}
