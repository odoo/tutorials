from odoo import api, fields, models
from datetime import timedelta

class WarrantyLineWizard(models.TransientModel):
    _name = 'warranty.line.wizard'
    _description = 'Defines single mapping between sales product and corresponding warranty'

    wizard_id = fields.Many2one("warranty.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_id = fields.Many2one("product.template", compute="_compute_product", string="Product")
    warranty_config_id = fields.Many2one("warranty.configuration", string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date", readonly=True)

    @api.depends("warranty_config_id")
    def _compute_end_date(self):
        for record in self:
            if record.warranty_config_id and record.warranty_config_id.year:
                record.end_date = fields.Date.today() + timedelta(
                    days=record.warranty_config_id.year * 365
                )
            else:
                record.warranty_config_id = None
                record.end_date = None

    @api.depends("sale_order_line_id")
    def _compute_product(self):
        for record in self:
            if record.sale_order_line_id:
                record.product_id = record.sale_order_line_id.product_template_id
            else:
                record.product_id = False
