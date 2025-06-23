from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ImportDetailWizard(models.TransientModel):
    _name = "import.export.details.wizard"
    _description = "Import Duty Detail Line"

    # ===== RELATIONSHIP FIELDS =====
    # Parent wizard reference - must be defined first for related fields
    parent_wizard_id = fields.Many2one(
        "import.export.wizard",
        string="Parent Wizard Reference",
        ondelete="cascade",
    )
    # Source invoice line being processed
    invoice_line_id = fields.Many2one(
        "account.move.line",
        string="Invoice Line",
        required=True,
    )
    # Currency for monetary field calculations
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="parent_wizard_id.currency_id",
        store=True,
    )

    # ===== UI COLUMN 1: PRODUCT =====
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        related="invoice_line_id.product_id",
    )
    # Hidden product information (not visible in columns)
    quantity = fields.Float(string="Quantity", related="invoice_line_id.quantity")
    price_unit = fields.Float(string="Unit Price", related="invoice_line_id.price_unit")
    exchange_rate = fields.Monetary(
        string="Exchange Rate",
        currency_field="currency_id",
        related="parent_wizard_id.currency_rate",
    )

    # ===== UI COLUMN 2: ASSESSABLE VALUE =====
    assessable_value = fields.Monetary(
        string="Assessable Value",
        currency_field="currency_id",
        compute="_compute_import_assessable_value",
        default=0.0,
    )

    # ===== UI COLUMN 3: CUSTOMS DUTY =====
    customs_duty_amount = fields.Monetary(
        string="Customs Duty & Charges",
        currency_field="currency_id",
        default=0.0,
    )

    # ===== UI COLUMN 4: TAXABLE AMOUNT =====
    taxable_amount = fields.Monetary(
        string="Taxable Amount",
        currency_field="currency_id",
        compute="_compute_import_taxable_amount",
        default=0.0,
    )

    # ===== UI COLUMN 5: IMPORT TAXES =====
    import_tax_ids = fields.Many2many(
        "account.tax",
        string="Import Taxes",
        domain=[("type_tax_use", "=", "purchase")],
    )

    # ===== UI COLUMN 6: TAX AMOUNT =====
    tax_amount = fields.Monetary(
        string="Tax Amount",
        currency_field="currency_id",
        compute="_compute_import_tax_amount",
        default=0.0,
    )

    @api.constrains("customs_duty_amount")
    def _validate_customs_duty_amount_positive(self):
        for record in self:
            if record.customs_duty_amount < 0:
                raise ValidationError("Customs Duty cannot be a negative amount.")

    @api.depends("quantity", "price_unit", "parent_wizard_id.currency_rate")
    def _compute_import_assessable_value(self):
        """Calculate assessable value based on quantity, price and exchange rate"""
        for record in self:
            record.assessable_value = (
                record.quantity
                * record.price_unit
                * record.parent_wizard_id.currency_rate
            )

    @api.depends("assessable_value", "customs_duty_amount")
    def _compute_import_taxable_amount(self):
        for record in self:
            record.taxable_amount = record.assessable_value + record.customs_duty_amount

    @api.depends("taxable_amount", "import_tax_ids")
    def _compute_import_tax_amount(self):
        for record in self:
            tax_factor = (
                sum(record.import_tax_ids.mapped("amount")) / 100
                if record.import_tax_ids
                else 0.0
            )
            record.tax_amount = record.taxable_amount * tax_factor
