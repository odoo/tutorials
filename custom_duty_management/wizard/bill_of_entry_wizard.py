from odoo import api, fields, models


class BillOfEntryWizard(models.TransientModel):
    _name = "bill.of.entry.wizard"
    _description = "Bill of Entry Wizard"

    move_id = fields.Many2one("account.move", string="Vendor Bill", required=True)
    journal_entry_no = fields.Char(string="Journal Entry No", readonly=True)
    journal_entry_date = fields.Date(
        string="Journal Entry Date", default=fields.Date.today, readonly=True
    )
    journal_id = fields.Many2one("account.journal", string="Journal", readonly=True)
    company_currency_id = fields.Many2one(
        "res.currency",
        string="Company Currency",
        default=lambda self: self.env.company.currency_id.id,
        readonly=True,
    )
    custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",
        required=True,
        currency_field="company_currency_id",
    )

    reference = fields.Char(string="Reference")
    bill_of_entry_no = fields.Char(string="Bill of Entry No")
    bill_of_entry_date = fields.Date(string="Bill of Entry Date")
    port_code = fields.Many2one("l10n_in.port.code", string="Port Code")

    line_ids = fields.One2many(
        "bill.of.entry.line.wizard", "wizard_id", string="Bill of Entry Details"
    )

    # Computed Fields
    total_custom_duty = fields.Monetary(
        string="Total Custom Duty + Additional Charges",
        compute="_compute_totals",
        store=True,
        currency_field="company_currency_id",
    )
    total_tax = fields.Monetary(
        string="Total Tax Amount",
        compute="_compute_totals",
        store=True,
        currency_field="company_currency_id",
    )
    total_amount_payable = fields.Monetary(
        string="Total Amount Payable",
        compute="_compute_totals",
        store=True,
        currency_field="company_currency_id",
    )

    @api.depends("line_ids", "custom_currency_rate")
    def _compute_totals(self):
        """Compute totals for custom duty, taxes, and total payable amount."""
        for wizard in self:
            total_duty = sum(line.custom_duty for line in wizard.line_ids)
            total_tax = sum(line.tax_amount for line in wizard.line_ids)
            wizard.total_custom_duty = total_duty * wizard.custom_currency_rate
            wizard.total_tax = total_tax * wizard.custom_currency_rate
            wizard.total_amount_payable = (total_duty + total_tax) * wizard.custom_currency_rate

    @api.model
    def default_get(self, fields_list):
        """Set default values when opening the wizard and copy bill lines."""
        defaults = super().default_get(fields_list)
        move_id = self.env.context.get("default_move_id")
        company = self.env.company
        default_journal = company.l10n_in_import_journal_id

        custom_currency_rate = company.currency_id.rate

        if move_id:
            move = self.env["account.move"].browse(move_id)
            existing_wizard = self.search([("move_id", "=", move.id)], limit=1)

            if existing_wizard:
                return existing_wizard.read(fields_list)[0]

            defaults.update(
                {
                    "move_id": move.id,
                    "reference": move.ref,
                    "bill_of_entry_no": move.l10n_in_shipping_bill_number,
                    "bill_of_entry_date": move.l10n_in_shipping_bill_date,
                    "port_code": move.l10n_in_shipping_port_code_id.id,
                    "journal_id": default_journal.id if default_journal else False,
                    "custom_currency_rate": custom_currency_rate,
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
                            "tax_id": line.tax_ids and line.tax_ids[0].id or False,
                        }
                    )
                )
            defaults["line_ids"] = line_values

        return defaults

    def action_confirm(self):
        """Placeholder function for confirm button."""
        return {"type": "ir.actions.act_window_close"}
