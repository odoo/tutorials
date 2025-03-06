# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = "productkit"
    _description = "Product Kit Wizard"

    product_id = fields.Many2one(comodel_name="product.product")
    order_line_id = fields.Many2one(comodel_name="sale.order.line")
    kit_product_ids = fields.One2many("productkit.line", "kit_product_line_id")

    @api.model
    def default_get(self, fields_list):
        res = super(ProductKitWizard, self).default_get(fields_list)

        if not res.get("order_line_id"):
            return res

        order_line = self.env["sale.order.line"].browse(res["order_line_id"])
        print("orderline", order_line)
        product = order_line.product_id
        print("product", product)
        kit_products = []

        if product.product_template_id.has_kit:

            existing_kit_lines = self.env["productkit.line"].search(
                [("kit_product_line_id.order_line_id", "=", order_line.id)]
            )
            print(existing_kit_lines)

            existing_kit_data = {line.product_id.id: line for line in existing_kit_lines}

            for sub_product in product.product_tmpl_id.kit_products:
                if sub_product.id in existing_kit_data:
                    # Use previously set values if available
                    existing_line = existing_kit_data[sub_product.id]
                    kit_products.append((0, 0, {
                        'product_id': existing_line.product_id.id,
                        'kit_product_name': existing_line.kit_product_name,
                        'kit_product_qty': existing_line.kit_product_qty,
                        'kit_product_price': existing_line.kit_product_price,
                    }))
                else:
                    kit_products.append((0, 0, {
                        'product_id': sub_product.id,
                        'kit_product_name': sub_product.name,
                        'kit_product_qty': 1,
                        'kit_product_price': sub_product.lst_price,
                    }))

        res['kit_product_ids'] = kit_products
        return res
