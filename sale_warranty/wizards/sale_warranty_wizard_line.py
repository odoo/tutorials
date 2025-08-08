from odoo import api, fields, models


class SaleWarrantyWizardLine(models.TransientModel):
    _name = 'sale.warranty.wizard.line'
    _description = 'Wizard Line to choose warranty config for the product'

    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    warranty_configuration_id = fields.Many2one(comodel_name='sale.warranty.configuration', string='Year')
    end_date = fields.Date(string='End Date', compute="_compute_end_date")
    quantity = fields.Float()
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')

    warranty_wizard_id = fields.Many2one(comodel_name='sale.warranty.wizard', string='Warranty Wizard')

    @api.depends('warranty_configuration_id')
    def _compute_end_date(self):
        for line in self:
            line.end_date = fields.Date.add(fields.Date.today(),years=line.warranty_configuration_id.year)
