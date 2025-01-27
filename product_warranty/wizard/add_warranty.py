from odoo import api, fields, models


class add_warranty(models.TransientModel):
    _name = "product.add.warranty"
    _description = "product.warranty.configuration"

    list_warranty_ids = fields.One2many(
        "product.list.warranty", "add_warranty_id", string="product warranties"
    )

    @api.model
    def default_get(self, default_fields):
        defaults = super().default_get(default_fields)
        default_product = self.env.context.get("product_ids")
        ids = []
        for product_id in default_product:
            ids.append(
                {
                    "product_id": product_id[0],
                    "qty": product_id[1],
                    "order_line_id": product_id[2],
                },
            )
        warranty_ids = self.env["product.list.warranty"].create(ids)
        defaults["list_warranty_ids"] = warranty_ids
        return defaults
        

    @api.model_create_multi
    def create(self, vals_list):
        vals = super().create(vals_list)
        sale_order = self.env["sale.order"].search(
            [("id", "=", self.env.context.get("active_id"))]
        )
        for record in vals:
            for warranty in record.list_warranty_ids:
                if warranty.warranty_id:
                    warranty_price = (
                        warranty.warranty_id.percentage / 100
                    ) * warranty.product_id.list_price
                    self.env["sale.order.line"].create(
                        {
                            "order_id": sale_order.id,
                            "product_id": warranty.warranty_id.product_template_id.product_variant_id.id,
                            "name": warranty.warranty_id.product_template_id.name,
                            "product_uom_qty": warranty.qty,
                            "price_unit": warranty_price,
                            "link_product_id": warranty.order_line_id,
                        }
                    )

        return vals
