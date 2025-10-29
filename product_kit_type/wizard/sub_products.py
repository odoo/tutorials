from odoo import models, fields, api


class SubProductsWizard(models.TransientModel):
    _name = "product_kit_type.subproducts"
    _description = "Sub Products"

    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    sub_product_line_ids = fields.One2many("product_kit_type.subproducts.line", "wizard_id", string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_order_line = self.env["sale.order.line"].browse(self.env.context.get("active_id"))

        if sale_order_line:
            res["sale_order_line_id"] = sale_order_line.id

        existing_lines = self.env["sale.order.line"].search([
            ("linked_line_id", "=", sale_order_line.id),
            ("is_sub_product", "=", True)
        ])

        sub_product_lines = []
        if existing_lines:
            for line in existing_lines:
                sub_product_lines.append((0, 0, {
                    "product_id": line.product_id.id,
                    "product_qty": line.product_uom_qty,
                    "price_unit": line.product_id.list_price,
                }))
        else:
            for sub_product in sale_order_line.product_template_id.sub_products:
                sub_product_lines.append((0, 0, {
                    "product_id": sub_product.id,
                    "product_qty": 1,
                    "price_unit": sub_product.list_price,
                }))

        res["sub_product_line_ids"] = sub_product_lines
        return res

    def action_confirm(self):
        self.ensure_one()
        sale_order = self.sale_order_line_id.order_id
        existing_sub_lines = sale_order.order_line.filtered(lambda line: line.is_sub_product and line.linked_line_id.id == self.sale_order_line_id.id)
        existing_sub_product_map = {line.product_id.id: line for line in existing_sub_lines}
        total_price = 0

        for sub_product in self.sub_product_line_ids:
            if sub_product.product_id.id in existing_sub_product_map:
                existing_line = existing_sub_product_map[sub_product.product_id.id]
                existing_line.write({
                    "product_uom_qty": sub_product.product_qty,
                    "price_unit": 0.00,
                })
            else:
                self.env["sale.order.line"].create({
                    "name": sub_product.product_id.name,
                    "order_id": self.sale_order_line_id.order_id.id,
                    "product_id": sub_product.product_id.id,
                    "product_uom_qty": sub_product.product_qty,
                    "price_unit": 0.00,
                    "is_sub_product": True,
                    'linked_line_id': self.sale_order_line_id.id,
                })

            total_price += sub_product.product_qty * sub_product.price_unit

        self.sale_order_line_id.write({'price_unit': total_price})

        return {"type": "ir.actions.act_window_close"}
