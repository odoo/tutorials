from odoo import api, fields, models


class BillOfEntryWizardLine(models.TransientModel):
    _name = "bill.of.entry.line.wizard"
    _description = "Bill of Entry Wizard Line"

    price_unit_foreign = fields.Float(string="Unit Price", readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)

    wizard_id = fields.Many2one(
        "bill.of.entry.wizard", string="Wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    company_currency_id = fields.Many2one(
        "res.currency", related="wizard_id.company_currency_id", readonly=True
    )
    custom_currency_rate = fields.Monetary(
        related="wizard_id.custom_currency_rate",
        currency_field="company_currency_id",
        readonly=True,
    )
    tax_id = fields.Many2one("account.tax", string="Taxes")

    assessable_value = fields.Monetary(
        string="Assessable Value",
        compute="_compute_values",
        currency_field="company_currency_id",
        # store=True,
    )
    custom_duty = fields.Monetary(
        string="Custom Duty + Additional Charges", currency_field="company_currency_id"
    )
    taxable_amount = fields.Monetary(
        string="Taxable Amount",
        compute="_compute_values",
        currency_field="company_currency_id",
    )
    tax_amount = fields.Monetary(
        string="Tax Amount",
        compute="_compute_values",
        currency_field="company_currency_id",
    )

    @api.depends("price_unit_foreign", "quantity", "custom_currency_rate")
    def _compute_values(self):
        """Compute assessable value, custom duty, and tax amount based on currency rate."""
        for line in self:
            rate = line.custom_currency_rate or 1.0
            if line.price_unit_foreign and line.quantity:
                line.assessable_value = (
                    line.quantity * line.price_unit_foreign
                ) * rate  # Convert to INR
            else:
                line.assessable_value = 0.0

            line.taxable_amount = line.assessable_value + line.custom_duty
            if line.tax_id:
                line.tax_amount = (line.taxable_amount * line.tax_id.amount) / 100
            else:
                line.tax_amount = 0.0

    @api.onchange("custom_duty", "custom_currency_rate")
    def _onchange_recompute_values(self):
        for line in self:
            line._compute_values()
