from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class WarrantyLine(models.TransientModel):
    _name = 'warranty.line'
    _description = "Warranty line"

    product_warranty_id = fields.Many2one(
        'product.warranty',
        string="Wizard",
        required=True
    )
    sale_order_line_id = fields.Many2one(
        'sale.order.line',
        required=True,
    )
    product_template_id = fields.Many2one(
        related='sale_order_line_id.product_template_id'
    )
    product_warranty_config_id = fields.Many2one(
        'product.warranty.config',
        string="Warranty"
    )
    end_date = fields.Date(
        string="End Date",
        compute='_compute_end_date'
    )

    @api.depends('product_warranty_config_id.year')
    def _compute_end_date(self):
        for line in self:
            if line.product_warranty_config_id:
                line.end_date = datetime.today() + relativedelta(years=line.product_warranty_config_id.year)
            else:
                line.end_date = False
