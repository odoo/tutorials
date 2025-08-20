# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductWarrantyLinesWizard(models.TransientModel):
    _name = "product.warranty.wizard.lines"
    _description = "Product Warranty Wizard Lines"

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product",
        ondelete="cascade", readonly=True
    )
    end_date = fields.Text(
        string="Warranty EndDate", store=True,
        compute="_compute_end_date"
    )
    warranty_config_id = fields.Many2one(
        comodel_name="product.warranty.config",
        string="Warranty Configuration",
        help="Select the warranty configuration for this product"
    )
    wizard_id = fields.Many2one(
        comodel_name="product.warranty.wizard",
        string="Wizard Reference", readonly=True,
        help="Reference to the parent wizard"
    )
    sale_order_line_id = fields.Many2one("sale.order.line", string="Original Order Line")

    @api.depends("warranty_config_id")
    def _compute_end_date(self):
        for line in self:
            line.end_date = (
                fields.Date.add(fields.Date.today(), years=line.warranty_config_id.year)
                if line.warranty_config_id
                else "No warranty configuration selected"
            )
