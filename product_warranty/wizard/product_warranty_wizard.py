# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, api, fields, models
from odoo.exceptions import UserError


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "Product Warranty Wizard"

    wizard_line_ids = fields.One2many(
        comodel_name="product.warranty.wizard.lines",
        inverse_name="wizard_id", string="Warranty Lines",
        help="Lines for adding warranty products"
    )
    sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Sale Order",
        help="Reference to the sale order for which warranty products are being added"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order = self.env["sale.order"].browse(
            self.env.context.get("default_sale_order_id")
        )
        sale_order_line_id = sale_order.order_line.filtered(
            lambda l: l.product_template_id.warranty
        )
        res["wizard_line_ids"] = [
            Command.create({"product_id": line.product_id.id, "sale_order_line_id": line.id})
            for line in sale_order_line_id
        ]
        return res

    def action_add_warranty(self):
        for line in self.wizard_line_ids:
            if not line.warranty_config_id:
                raise UserError(_("Warranty Configuration is required for all warranty lines."))

        warranty_lines = []
        for line in self.wizard_line_ids:
            base_price = line.sale_order_line_id.price_unit
            warranty_price = base_price * (line.warranty_config_id.percentage / 100.0)
            warranty_lines.append({
                "order_id": self.sale_order_id.id,
                "product_id": line.warranty_config_id.product_id.id,
                "name": "End Date:" + line.end_date,
                "price_unit": warranty_price,
                "product_uom_qty": 1.0,
                "source_order_line_id": line.sale_order_line_id.id,
                "sequence": line.sale_order_line_id.sequence,
            })
        if warranty_lines:
            self.env["sale.order.line"].create(warranty_lines)
