from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class WarrantyWizardLine(models.TransientModel):
    _name = "product.warranty.wizard.line"
    _description = "Warranty Wizard Line"

    wizard_id = fields.Many2one("product.warranty.add.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_template_id = fields.Many2one(
        "product.template", string="Product", related="sale_order_line_id.product_template_id", readonly=True 
    )
    warranty_config_id = fields.Many2one(
        "product.warranty", string="Warranty Type" 
    )
    date_end = fields.Date(string="Date End", compute="_compute_product_date_end")

    @api.depends("warranty_config_id.years")
    def _compute_product_date_end(self):
        for line in self:
            if line.warranty_config_id:
                line.date_end = datetime.today() + relativedelta(
                    days = line.warranty_config_id.years * 365
                )
            else:
                line.date_end = False    
