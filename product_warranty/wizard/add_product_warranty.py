from odoo import api, Command, fields, models


class AddProductWarranty(models.TransientModel):
    _name = "add.product.warranty"
    _description = "Add product warranty wizard"

    @api.model
    def default_get(self, fields_list):
        """Fetches active sale order id and creates warranty lines linked with order lines"""
        res = super().default_get(fields_list)
        sale_order_id = self.env.context.get("active_id")
        
        if sale_order_id:
            order_lines = self.env["sale.order"].browse(sale_order_id).order_line
            res["warranty_line_ids"] = [
                Command.create({"sale_order_line_id": order_line.id})
                for order_line in order_lines.filtered(lambda ol: ol.product_template_id.is_warranty_available)
            ]
                       
        res["sale_order_id"] = sale_order_id
        return res

    sale_order_id = fields.Many2one(comodel_name="sale.order", required=True)
    warranty_line_ids = fields.One2many(comodel_name="product.warranty.line", inverse_name="wizard_id")

    def action_add_warranty(self):
        for warranty_line in self.warranty_line_ids:
            if warranty_line.warranty_configuration_id:
                self.env["sale.order.line"].create({
                    "product_id": warranty_line.warranty_configuration_id.product_id.product_variant_id.id,
                    "product_uom_qty": warranty_line.sale_order_line_id.product_uom_qty,
                    "order_id": self.sale_order_id.id,
                    "price_unit": warranty_line.sale_order_line_id.price_unit * (warranty_line.warranty_configuration_id.percentage / 100),
                    "linked_line_id": warranty_line.sale_order_line_id.id,
                    "name": f"For {warranty_line.sale_order_line_id.name}\nEnd Date: {warranty_line.warranty_end_date}",
                    "sequence": warranty_line.sale_order_line_id.sequence + 1
                })