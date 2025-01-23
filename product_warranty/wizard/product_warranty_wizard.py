from odoo import api, Command, fields, models


class WarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "Warranty Selection Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    line_ids = fields.One2many(
        "product.warranty.wizard.line", "wizard_id", string="Warranty Lines"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))
        warranty_lines = []

        for line in sale_order.order_line.filtered(
            lambda line: line.product_template_id
            and line.product_template_id.is_warranty_product
        ):
            warranty_lines.append(
                Command.create(
                    {
                        "sale_order_line_id": line.id,
                        "warranty_config_id": False,
                    }
                )
            )
        res["sale_order_id"] = sale_order.id
        res["line_ids"] = warranty_lines
        return res

    def apply_warranty(self):
        for line in self.line_ids:
            product = self.env["product.template"].browse(line.product_template_id.id)
            if line.warranty_config_id:
                self.env["sale.order.line"].create(
                    {
                        "order_id": self.sale_order_id.id,
                        "product_template_id": line.warranty_config_id.product_template_id.id,
                        "name": "Extended Warranty of %d Years - %s"
                        % (line.warranty_config_id.years, product.name),
                        "product_uom_qty": 1,
                        "linked_line_id": line.sale_order_line_id.id,
                        "price_unit": (line.warranty_config_id.percentage / 100)
                        * line.sale_order_line_id.price_subtotal,
                    }
                )

        return {"type": "ir.actions.act_window_close"}
