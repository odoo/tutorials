from odoo import models, fields, api
from datetime import timedelta


class AddWarrantyLineWizard(models.TransientModel):
    _name = 'add.warranty.line.wizard'
    _description = 'Add Warranty Line Wizard'

    wizard_id = fields.Many2one('add.warranty.wizard', string="Wizard")

    sale_order_line_id = fields.Many2one("sale.order.line", string = "Sale Order Line")

    product_id = fields.Many2one(
        "product.template", compute="_compute_product_name", string="Product"
    )

    warranty_config_id = fields.Many2one('warranty.configuration', string="Year")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("sale_order_line_id")
    def _compute_product_name(self):
        for record in self:
            if record.sale_order_line_id:
                record.product_id = record.sale_order_line_id.product_template_id
            else:
                record.product_id = False
                
    @api.depends('warranty_config_id')
    def _compute_end_date(self):
        for record in self:
            if record.warranty_config_id and record.warranty_config_id.duration:
                record.end_date = fields.Date.today() + timedelta(days=record.warranty_config_id.duration * 365)
            else:
                record.end_date = False
