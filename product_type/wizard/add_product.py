from odoo import api, fields, models


class add_product(models.TransientModel):
    _name = "product.add.product"
    _description = "product.add.product"

    name = fields.Char(String="Product name", requried=True, readonly=True)
    pid = fields.Integer()
    sale_order_id = fields.Integer(required=True)

    is_create = fields.Boolean()
    list_product_ids = fields.One2many(
        "product.list.product", "add_product_id", string="product warranties"
    )

    @api.model
    def default_get(self, default_fields):
        defaults = super().default_get(default_fields)
        default_product = self.env.context.get("product_ids")
        defaults["name"] = self.env.context.get("pname")
        defaults["sale_order_id"] = self.env.context.get("sale_order_id")
        defaults["pid"] = self.env.context.get("active_id")
        ids = []
        for product_id in default_product:
            print(product_id[0])
            ids.append(
                {
                    "product_id": product_id[0],
                    "qty": product_id[1],
                    "price": product_id[2],
                    "order_line_id": product_id[3],
                },
            )
        warranty_ids = self.env["product.list.product"].create(ids)
        defaults["list_product_ids"] = warranty_ids
        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        vals = super().create(vals_list)
        sale_order = self.env["sale.order"].search([("id", "=", vals.sale_order_id)])
        for record in vals:
            order_line = sale_order.order_line.search([("id", "=", vals.pid)])
            
            order_line.price_unit = 0
            data = []
            for val in record.list_product_ids:
                order_line.price_unit += val.price * val.qty
                temp = {
                    "order_id": sale_order.id,
                    "product_id": val.product_id.id,
                    "name": ("%s sub product" % val.product_id.name,),
                    "product_uom_qty": val.qty,
                    "price_unit": 0,
                    "linked_line_id": vals.pid,
                }
                if order_line.linked_line_ids:
                    self.env["sale.order.line"].browse(val.order_line_id).write(temp)
                else:
                    data.append(temp)

            if order_line.linked_line_ids:
                    self.env["sale.order.line"].create(data)

        return vals
