from odoo import fields, models, api, Command


class SubProductKitWizard(models.TransientModel):
    _name = 'sub.product.kit.wizard'

    sale_order_line_id = fields.Many2one('sale.order.line', required=True)
    sub_products_ids = fields.One2many('sub.product.line.kit.wizard', 'sub_products_line_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self._context.get("active_id")
        if sale_order_line_id:
            sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
            existing_lines = self.env["sale.order.line"].search([
                ("main_product_line_id", "=", sale_order_line_id)
            ])
            sub_product_line_wizard = self.env["sub.product.line.kit.wizard"]
            line_values = []
            if existing_lines:
                vals_list = [
                    {
                        "product_id": line.product_id.id,
                        "price": line.price_unit,
                        "quantity": line.product_uom_qty,
                    }
                    for line in existing_lines
                ]
            else:
                vals_list = [
                    {
                        "product_id": sub_product.id,
                        "price": sub_product.list_price,
                        "quantity": 1,
                    }
                    for sub_product in sale_order_line.product_id.sub_products_ids
                ]
            if vals_list:
                curr_products = sub_product_line_wizard.create(vals_list)
                line_values = [Command.link(product.id) for product in curr_products]
            res.update({
                "sub_products_ids": line_values,
                "sale_order_line_id": sale_order_line_id,
            })
        return res

    def action_confirm(self):
        existing_sub_product_lines_map = {
            line.product_id.id: line
            for line in self.env["sale.order.line"].search(
                [
                    ("main_product_line_id", "=", self.sale_order_line_id.id),
                    ("order_id", "=", self.sale_order_line_id.order_id.id)
                ]
            )
        }
        total_of_sub_product_price = 0
        for rec in self.sub_products_ids:
            product_id = rec.product_id.id
            existing_line = existing_sub_product_lines_map.get(product_id)
            if existing_line:
                existing_line.write({
                    "product_uom_qty": rec.quantity,
                    "last_price": rec.price,
                    "price_unit": 0,
                })
            else:
                self.env["sale.order.line"].create(
                    {
                        "order_id": self.sale_order_line_id.order_id.id,
                        "product_id": rec.product_id.id,
                        "product_uom_qty": rec.quantity,
                        "last_price": rec.price,
                        "price_unit": 0,
                        "main_product_line_id": self.sale_order_line_id.id,
                    }
                )
            total_of_sub_product_price += (rec.quantity * rec.price)
        total_of_sub_product_price += (
                self.sale_order_line_id.product_uom_qty
                * self.sale_order_line_id.product_template_id.list_price
        )
        self.sale_order_line_id.price_unit = total_of_sub_product_price
        return True
