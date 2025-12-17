from odoo import fields, models


class AccountMoveBillEntryLine(models.Model):
    _name = "account.move.bill.of.entry.line"
    _description = "Wizard Bill of Entry Line for Journal Entry"

    move_id = fields.Many2one("account.move", string="Journal entry", ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Product")
    tax_id = fields.Many2one("account.tax", string="Taxes", domain="[('type_tax_use', '=', 'purchase')]")
    currency_id = fields.Many2one("res.currency", related="move_id.company_currency_id")
    assessable_value = fields.Monetary(string="Assessable Value", store=True)
    custom_duty = fields.Monetary(string="Custom Duty + Additional Charges")
    taxable_amount = fields.Monetary(string="Taxable Amount",  store=True)
    tax_amount = fields.Monetary(string="Tax Amount", store=True)
