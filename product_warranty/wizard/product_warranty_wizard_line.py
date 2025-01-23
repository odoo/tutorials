from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class WarrantyWizardLine(models.TransientModel):
    _name = "product.warranty.wizard.line"
    _description = "Warranty Wizard Line"

    wizard_id = fields.Many2one("product.warranty.wizard", string="Wizard")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    product_template_id = fields.Many2one(
        "product.template", string="Product", compute="_compute_product_template_id"
    )
    warranty_config_id = fields.Many2one(
        "product.warranty.config", string="Warranty Type"
    )
    date_end = fields.Date(string="Date End", compute="_compute_date_end")

    @api.depends("warranty_config_id.years")
    def _compute_date_end(self):
        for line in self:
            line.date_end = datetime.today() + relativedelta(
                years=line.warranty_config_id.years
            )

    @api.depends("sale_order_line_id")
    def _compute_product_template_id(self):
        for line in self:
            if line.sale_order_line_id:
                line.product_template_id = line.sale_order_line_id.product_template_id
            else:
                line.product_template_id = False
