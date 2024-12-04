from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class AddWarrantyLineWizard(models.TransientModel):
    _name = "add.warranty.line.wizard"
    _description = "Temporary line model for warranty in wizard"

    warranty_id = fields.Many2one(
        "add.warranty.wizard",
        string="Wizard Reference",
    )

    sale_order_line_id = fields.Many2one(
        "sale.order.line",
        string="SaleOrderLine",
    )

    product_id = fields.Many2one(
        "product.template", compute="_compute_product_name", string="Product"
    )

    warranty_config_id = fields.Many2one("warranty.configuration", string="Year")

    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("sale_order_line_id")
    def _compute_product_name(self):
        for record in self:
            if record.sale_order_line_id:
                record.product_id = record.sale_order_line_id.product_template_id
            else:
                record.product_id = False

    @api.depends("warranty_config_id")
    def _compute_end_date(self):
        today = date.today()
        for record in self:
            if record.warranty_config_id and record.warranty_config_id.year:
                record.end_date = today + relativedelta(
                    years=int(record.warranty_config_id.year)
                )
            else:
                record.end_date = False
