from odoo import api, fields, models, Command


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Product kit wizard view"

    wizard_sub_product_ids = fields.One2many(
        comodel_name="product.kit.line.wizard",
        inverse_name="wizard_id",
        string="Sub Products",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        sale_order_line = self.env["sale.order.line"].browse(active_id)
        existing_products = sale_order_line.linked_line_ids.product_id
        sub_product_lines = []
        
        for sub_product in sale_order_line.product_template_id.sub_product_ids:
            if sub_product in existing_products:
                sub_product_order_line = self.env["sale.order.line"].search([
                    ("order_id", "=", sale_order_line.order_id.id), 
                    ("product_id", "=", sub_product.id),
                    ("linked_line_id", "=", sale_order_line.id)  
                ])
                sub_product_lines.append(
                    Command.create({
                        "product_id": sub_product.id,
                        "quantity": sub_product_order_line.product_uom_qty , 
                        "price": sub_product_order_line.wizard_price,
                    })
                )
            else:
                sub_product_lines.append(
                    Command.create({
                        "product_id": sub_product.id,
                        "quantity": 1, 
                        "price": sub_product.product_tmpl_id.list_price,
                    })
                )

        res["wizard_sub_product_ids"]= sub_product_lines
        return res

    def action_confirm(self):
        active_id = self.env.context.get("active_id")
        sale_order_line = self.env["sale.order.line"].browse(active_id)
        sale_order_line.linked_line_ids.unlink()
        total_price = 0
        line_commands = []

        for wizard_line in self.wizard_sub_product_ids:
            line_commands.append(Command.create({
                'product_id': wizard_line.product_id.id,
                'product_uom_qty': wizard_line.quantity,
                'wizard_price':wizard_line.price,
                'price_unit': 0,
                'linked_line_id': sale_order_line.id,
            }))
            total_price += wizard_line.price * wizard_line.quantity
            
        sale_order_line.order_id.write({'order_line': line_commands})
        sale_order_line.write({'price_unit': total_price})
