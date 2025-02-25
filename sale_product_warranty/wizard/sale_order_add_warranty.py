from odoo import api, Command, fields, models

class SaleOrderAddWarranty(models.TransientModel):
    _name = "sale.order.add.warranty"
    _description = "Add Warranty Wizard"

    sale_order_id = fields.Many2one("sale.order", required=True, ondelete="cascade")
    warranty_line_ids = fields.One2many("sale.order.add.warranty.line", "wizard_id")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))

        warranty_lines = []
        for line in sale_order.order_line:
            has_warranty = self.env["sale.order.line"].search_count([("warranty_linked_with_product_id", "=", line.id)]) > 0
            if line.product_id.is_warranty_available and not has_warranty:
                warranty_lines.append({
                    "product_id": line.product_id.id,
                    "sale_order_line_id": line.id,
                })

        res.update({
            "sale_order_id": sale_order.id,
            "warranty_line_ids": [Command.clear()] + [Command.create(vals) for vals in warranty_lines],
        })
        return res

    def action_add_warranty(self):
        sale_order_lines = []
        warranty_lines = self.warranty_line_ids.filtered(lambda w: w.warranty_id)
        for line in warranty_lines:
            sale_order_lines.append({
                "product_id": line.warranty_id.product_id.id,
                "order_id": self.sale_order_id.id,
                "name": f" Extended Warranty, \n End Date: {line.end_date}",
                "price_unit": line.sale_order_line_id.price_unit * line.warranty_id.percentage / 100,
                "product_uom_qty": line.sale_order_line_id.product_uom_qty,
                'warranty_linked_with_product_id': line.sale_order_line_id.id,
                "sequence": line.sale_order_line_id.sequence,
            })
        if sale_order_lines:
            self.env["sale.order.line"].create(sale_order_lines)
        return
