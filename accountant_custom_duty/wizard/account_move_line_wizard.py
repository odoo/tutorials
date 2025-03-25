from odoo import api, fields, models


class AccountMoveLineWizard(models.TransientModel):
    _name = "account.move.line.wizard"
    _description = "Account Move Line Wizard"

    wizard_id = fields.Many2one("account.bill.of.entry.wizard", string="Wizard", required=True, ondelete="cascade")
    l10n_in_company_currency_id = fields.Many2one("res.currency", related="wizard_id.l10n_in_company_currency_id", string="Company Currency", readonly=True)
    account_id = fields.Many2one("account.account", string="Account")
    label = fields.Char(string="Label")
    debit = fields.Monetary(string="Debit", currency_field="l10n_in_company_currency_id")
    credit = fields.Monetary(string="Credit", currency_field="l10n_in_company_currency_id")

    product_id = fields.Many2one("product.product", string="Product")
    name = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
    price_unit = fields.Monetary(string="Unit Price", currency_field="l10n_in_company_currency_id")
    tax_ids = fields.Many2many("account.tax", string="Taxes", domain=[("type_tax_use", "=", "purchase")])

    l10n_in_custom_currency_rate = fields.Monetary(string="Custom Currency Rate", related="wizard_id.l10n_in_custom_currency_rate", currency_field="l10n_in_company_currency_id", readonly=True)

    l10n_in_assessable_value = fields.Monetary(string="Assessable Value", compute="_compute_l10n_in_assessable_value", store=True, currency_field="l10n_in_company_currency_id")

    l10n_in_custom_duty_additional = fields.Monetary(string="Custom Duty + Additional Charges", currency_field="l10n_in_company_currency_id", help="Enter any additional custom duty charges manually.")

    l10n_in_taxable_amount = fields.Monetary(string="Taxable Amount", compute="_compute_l10n_in_taxable_amount", store=True, currency_field="l10n_in_company_currency_id")

    l10n_in_tax_amount = fields.Monetary(string="Tax Amount", compute="_compute_l10n_in_tax_amount", store=True, currency_field="l10n_in_company_currency_id")

    @api.depends("quantity", "price_unit", "l10n_in_custom_currency_rate")
    def _compute_l10n_in_assessable_value(self):
        for line in self:
            line.l10n_in_assessable_value = (line.quantity * line.price_unit * line.l10n_in_custom_currency_rate)

    @api.depends("l10n_in_assessable_value", "l10n_in_custom_duty_additional")
    def _compute_l10n_in_taxable_amount(self):
        for line in self:
            line.l10n_in_taxable_amount = (line.l10n_in_assessable_value + line.l10n_in_custom_duty_additional)

    @api.depends("l10n_in_taxable_amount", "tax_ids")
    def _compute_l10n_in_tax_amount(self):
        for line in self:
            line.l10n_in_tax_amount = sum((line.l10n_in_taxable_amount * tax.amount) / 100 for tax in line.tax_ids)
