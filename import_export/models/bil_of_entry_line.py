from odoo import api, fields, models


class BillOfEntryLine(models.Model):
    _name = "bill.of.entry.line"
    _description = "Bill of Entry Line"

    bill_of_entry_id = fields.Many2one(comodel_name="bill.of.entry")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Details",
    )
    price_subtotal = fields.Float(help="Price Subtotal of product in account move line")
    assessable_value = fields.Monetary(
        string="Assessable Value",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency", related="bill_of_entry_id.currency_id"
    )
    custom_duty_additional_charge = fields.Monetary(
        string="Custom Duty + Additional Charges",
        store=True,
    )
    taxable_amount = fields.Monetary(
        string="Taxable Amount", compute="_compute_taxable_amount",store=True
    )
    tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Tax",
        domain=[("type_tax_use", "=", "purchase")],
        readonly=False,
        store=True
    )
    tax_amount = fields.Monetary(
        string="Tax Amount", compute="_compute_tax_amount", store=True
    )
    country_id=fields.Many2one(comodel_name="res.country",compute="set_country_id",store=True)
    is_confirmed_boe=fields.Boolean(related="bill_of_entry_id.is_confirmed_boe")
    journal_date=fields.Date(related="bill_of_entry_id.journal_entry_date")

    
    @api.depends(
        "bill_of_entry_id.custom_currency_rate",
        "price_subtotal",
        "custom_duty_additional_charge",
    )
    def _compute_taxable_amount(self):
        for record in self:
            record.taxable_amount = (
                record.assessable_value + record.custom_duty_additional_charge
            )

    @api.depends("bill_of_entry_id.country_id")
    def set_country_id(self):
        for rec in self:
            if rec.bill_of_entry_id.country_id:
                rec.country_id=rec.bill_of_entry_id.country_id

    @api.depends("taxable_amount", "tax_id")
    def _compute_tax_amount(self):
        for line in self:
            tax_amount = 0
            line.taxable_amount = (
                line.assessable_value + line.custom_duty_additional_charge
            )
            if line.tax_id:
                tax_amount = line._tax_compute_helper(line.taxable_amount, line.tax_id)
            line.tax_amount = (
                line.tax_id.amount * line.taxable_amount / 100
                if tax_amount == 0
                else tax_amount
            )

    def _tax_compute_helper(self, taxable_amount, tax_id):
        taxes_res = tax_id.compute_all(
            taxable_amount,
            currency=self.currency_id,
            quantity=1.0,
            product=False,
            partner=False,
            is_refund=False,
        )
        tax_amount = taxes_res["total_included"] - taxes_res["total_excluded"]
        tax_amount = abs(tax_amount)
        return tax_amount
