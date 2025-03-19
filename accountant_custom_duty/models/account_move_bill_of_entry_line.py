from odoo import fields, models


class AccountMoveBillOfEntryLine(models.Model):
    _name = "account.move.bill.of.entry.line"
    _description = "Bill of Entry Line"

    move_id = fields.Many2one("account.move", string="Journal Entry")
    l10n_in_company_currency_id = fields.Many2one("res.currency", related="move_id.l10n_in_company_currency_id", string="Company Currency", readonly=True, default=lambda self: self.env.ref("base.INR"))
    account_id = fields.Many2one("account.account", string="Account")
    label = fields.Char(string="Label")
    debit = fields.Monetary(string="Debit", currency_field="l10n_in_company_currency_id")
    credit = fields.Monetary(string="Credit", currency_field="l10n_in_company_currency_id")

    product_id = fields.Many2one("product.product", string="Product")
    name = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
    price_unit = fields.Monetary(string="Unit Price", currency_field="l10n_in_company_currency_id")
    tax_ids = fields.Many2many("account.tax", string="Taxes", domain=[("type_tax_use", "=", "purchase")])

    l10n_in_custom_currency_rate = fields.Monetary(string="Custom Currency Rate", related="move_id.l10n_in_custom_currency_rate", currency_field="l10n_in_company_currency_id", readonly=True)
    l10n_in_assessable_value = fields.Monetary(string="Assessable Value", store=True, currency_field="l10n_in_company_currency_id")
    l10n_in_custom_duty_additional = fields.Monetary(string="Custom Duty + Additional Charges", currency_field="l10n_in_company_currency_id", help="Enter any additional custom duty charges manually.")
    l10n_in_taxable_amount = fields.Monetary(string="Taxable Amount", store=True, currency_field="l10n_in_company_currency_id")
    l10n_in_tax_amount = fields.Monetary(string="Tax Amount", store=True, currency_field="l10n_in_company_currency_id")

    l10n_in_shipping_bill_number = fields.Char(string="Shipping Bill Number", related="move_id.l10n_in_shipping_bill_number", readonly=True)
    l10n_in_shipping_bill_date = fields.Date(string="Shipping Bill Date", related="move_id.l10n_in_shipping_bill_date", readonly=True)
    l10n_in_shipping_port_code_id = fields.Many2one("l10n_in.port.code", string="Shipping Port Code", related="move_id.l10n_in_shipping_port_code_id", readonly=True)
