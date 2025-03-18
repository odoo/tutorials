from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BillEntryDetailsWizard(models.TransientModel):
    _name = 'bill.entry.details.wizard'
    _description = 'Bill Entry Details Wizard'

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    wizard_id = fields.Many2one('bill.entry.wizard', string="Wizard Reference", ondelete='cascade')
    move_line_id = fields.Many2one('account.move.line', string='Move Line', required=True)

    product_id = fields.Many2one('product.product', string='Product', related='move_line_id.product_id')
    quantity = fields.Float(string='Quantity', related='move_line_id.quantity')
    price_unit = fields.Float(string='Unit Price', related='move_line_id.price_unit')

    custom_currency_rate = fields.Monetary(string='Custom Currency Rate', currency_field='currency_id', related='wizard_id.custom_currency_rate')

    custom_duty = fields.Monetary(string='Custom Duty & Additional Charges', currency_field='currency_id', default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes', domain=[('type_tax_use', '=', 'purchase')])
    
    assessable_value = fields.Monetary(string='Assessable Value', currency_field='currency_id', compute='_compute_assessable_value', default=0.0)
    taxable_amount = fields.Monetary(string='Taxable Amount', currency_field='currency_id', compute='_compute_taxable_amount', default=0.0)
    tax_amount = fields.Monetary(string='Tax Amount', currency_field='currency_id', compute='_compute_tax_amount', default=0.0)
    
    @api.constrains('custom_duty')
    def _check_positive_values(self):
        for record in self:
            if record.custom_duty < 0:
                raise ValidationError("Custom Duty cannot be negative.")

    @api.depends('quantity', 'price_unit', 'wizard_id.custom_currency_rate')
    def _compute_assessable_value(self):
        for record in self:
            record.assessable_value = (
                record.quantity * record.price_unit * record.wizard_id.custom_currency_rate
            )

    @api.depends('assessable_value', 'custom_duty')
    def _compute_taxable_amount(self):
        for record in self:
            record.taxable_amount = record.assessable_value + record.custom_duty

    @api.depends('taxable_amount', 'tax_ids')
    def _compute_tax_amount(self):
        for record in self:
            tax_factor = sum(record.tax_ids.mapped('amount')) / 100 if record.tax_ids else 0.0
            record.tax_amount = record.taxable_amount * tax_factor
