from odoo import api, fields, models, Command

class SubProductWizard(models.TransientModel):
    _name = "sub.product.wizard"
    _description = "Wizard to add sub-products"
   
    product_id = fields.Many2one("product.product", required=True)
    existing_ids = fields.One2many("sub.product.line.wizard", "wizard_id")
   
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get("active_id")  
        if not sale_order_line_id:
            return res
        
        main_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        existing_sub_products = []

        if main_order_line.component_ids:
            for record in main_order_line.component_ids:
                existing_sub_products.append(Command.create({
                    "product_id": record.product_id.id,
                    "quantity": record.product_uom_qty,
                    "price": record.price_unit,
                    "order_line_id": record.id,  
                }))
        elif main_order_line.product_id.is_kit:
            for product in main_order_line.product_id.sub_products_ids:
                existing_sub_products.append(Command.create({
                    "product_id": product.id,
                    "quantity": 1.0,
                    "price": product.lst_price,
                }))

        res.update({
            "product_id": main_order_line.product_id.id,  
            "existing_ids": existing_sub_products,
        })
        return res

    def action_add_products(self):
        main_order_line = self.env["sale.order.line"].browse(
            self.env.context.get("active_id")
        )

        if not main_order_line:
            raise UserError("Sale order line not found!")

        existing_products = { line.product_id.id: line for line in main_order_line.component_ids }
        for sub_product in self.existing_ids:
            if sub_product.product_id.id in existing_products:
                existing_products[sub_product.product_id.id].write({
                "product_uom_qty": sub_product.quantity,
                "price_unit": sub_product.price,
            })
            else:
                self.env["sale.order.line"].create({
                "order_id": main_order_line.order_id.id,
                "product_id": sub_product.product_id.id,
                "price_unit": sub_product.price,
                "product_uom_qty": sub_product.quantity,
                "parent_id": main_order_line.id,
            })

        total_price = sum(product.quantity * product.price for product in self.existing_ids)
        main_order_line.write({"price_unit": total_price})
