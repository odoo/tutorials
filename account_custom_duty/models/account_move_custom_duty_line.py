from odoo import models, fields, api


class AccountMoveCustomDutyLine(models.Model):
    _name = "account.move.custom.duty.line"
    _description = "Custom Duty Line"

    move_id = fields.Many2one("account.move", string="Journal Entry", required=True, ondelete="cascade")
    move_line_id = fields.Many2one("account.move.line", string="Move Line", required=True)
    product_id = fields.Many2one("product.product", string="Product", related="move_line_id.product_id", store=True)
    quantity = fields.Float(string="Quantity", related="move_line_id.quantity", store=True)
    unit_price = fields.Float(string="Unit Price", related="move_line_id.price_unit", store=True)
    currency_id = fields.Many2one("res.currency", string="Currency", related="move_id.currency_id", store=True)
    custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="currency_id")
    assessable_value = fields.Monetary(string="Assessable Value", currency_field="currency_id", compute="_compute_assessable_value", store=True)
    custom_duty = fields.Monetary(string="Custom Duty & Additional Charges", currency_field="currency_id")
    taxable_amount = fields.Monetary(string="Taxable Amount", currency_field="currency_id", compute="_compute_taxable_amount", store=True)
    tax_ids = fields.Many2many("account.tax", string="Taxes", domain=[("type_tax_use", "=", "purchase")])
    tax_amount = fields.Monetary(string="Tax Amount", currency_field="currency_id", compute="_compute_tax_amount", store=True, default=0.0)

    @api.depends("quantity", "unit_price", "custom_currency_rate")
    def _compute_assessable_value(self):
        """Computes the assessable value for the custom duty line."""
        for record in self:
            record.assessable_value = record.quantity * record.unit_price * record.custom_currency_rate

    @api.depends("assessable_value", "custom_duty")
    def _compute_taxable_amount(self):
        """Computes the taxable amount for the custom duty line."""
        for record in self:
            record.taxable_amount = record.assessable_value + record.custom_duty

    @api.depends("taxable_amount", "tax_ids")
    def _compute_tax_amount(self):
        """Computes the total tax amount based on the taxable amount and applicable tax rates."""
        for record in self:
            if record.tax_ids:
                tax_multiplier = sum(record.tax_ids.mapped("amount")) / 100
                record.tax_amount = record.taxable_amount * tax_multiplier
