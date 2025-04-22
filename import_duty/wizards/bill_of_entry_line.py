from odoo import api, fields, models


class BillOfEntryLine(models.TransientModel):
    _name = 'bill.of.entry.line'
    _description = 'Bill of Entry Line'

    wizard_id = fields.Many2one('bill.of.entry', string="Wizard", required=True)

    product_id = fields.Many2one('product.product', string="Product", required=True)
    assessable_value = fields.Monetary(string="Assessable Value", required=True)
    custom_duty = fields.Monetary(string="Custom Duty")
    tax_id = fields.Many2one('account.tax', domain=[('type_tax_use', '=', 'purchase')], string="Tax")
    tax_amount = fields.Monetary(string="Tax Amount", compute="_compute_tax_amount", store=True)
    taxable_amount = fields.Monetary(string="Taxable Amount", compute="_compute_taxable_amount", store=True)

    currency_id = fields.Many2one(related='wizard_id.currency_id', store=True, readonly=True)

    @api.depends('assessable_value', 'custom_duty')
    def _compute_taxable_amount(self):
        for line in self:
            line.taxable_amount = line.assessable_value + line.custom_duty

    @api.depends('taxable_amount', 'tax_id')
    def _compute_tax_amount(self):
        for line in self:
            if line.tax_id:
                line.tax_amount = line.tax_id.compute_all(line.taxable_amount)['taxes'][0]['amount'] if line.taxable_amount else 0.0
            else:
                line.tax_amount = 0.0
