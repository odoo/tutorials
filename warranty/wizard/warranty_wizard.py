from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class WarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Add warranty to product"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    wizard_line_ids = fields.One2many("warranty.wizard.line", "wizard_id", string="Warranty Lines")

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        default_sale_order_id = self.env.context.get("default_sale_order_id")
        if not default_sale_order_id:
            raise UserError("No Sale Order found! Please open the wizard from a Sale Order.")

        sale_order = self.env["sale.order"].browse(default_sale_order_id)
        warranty_lines = []
        for sale_order_line in sale_order.order_line.filtered(lambda line: line.product_template_id and line.product_template_id.is_warranty_available):
            warranty_lines.append(
                Command.create({
                    'sale_order_line_id': sale_order_line,
                    'product_id': sale_order_line.product_id,
                    'warranty_configuration_id': False,
                })
            )
        result["sale_order_id"] = sale_order.id
        result["wizard_line_ids"] = warranty_lines
        return result

    def action_add_warranty_wizard(self):
        warranty_lines_to_create = []
        for line in self.wizard_line_ids:
            if line.warranty_configuration_id:
                warranty_lines_to_create.append({
                    'order_id': self.sale_order_id.id,
                    'product_id': line.warranty_configuration_id.product_id.id,
                    'name': f"Extended Warranty End Date: {line.end_date}, for {line.product_id.name}",
                    'product_uom_qty': 1,
                    'price_unit': (line.sale_order_line_id.price_subtotal * (line.warranty_configuration_id.percentage / 100)),
                    'linked_line_id': line.sale_order_line_id.id,
                })
        self.env["sale.order.line"].create(warranty_lines_to_create)
        return {"type": "ir.actions.act_window_close"}
