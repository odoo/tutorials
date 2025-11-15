from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_warranty_product = fields.Boolean(default=False)
    warranty_product_id = fields.Many2one(
        "warranty.config"
    )  # if it has warranty product then here it will be the warranty product
    warranty_order_line = fields.Many2one(
        "sale.order.line", ondelete="set null"
    )  # if it has warranty product here it will be the order line of warranty
    is_warranty_product = fields.Boolean(default=False)
    product_with_warranty_order_line = fields.Many2one("sale.order.line", ondelete="cascade")

    @api.ondelete(at_uninstall=False)
    def _unlink_warranty_from_product(self):
        for record in self:
            if record.is_warranty_product:
                product = record.product_with_warranty_order_line
                product.has_warranty_product = False
                product.warranty_product_id = None
                product.warranty_order_line = None

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get("is_warranty_product",False):
                orders = self.env["sale.order.line"].search(
                    [
                        ("order_id", "=", val["order_id"]),
                        ("sequence", ">", val["sequence"] - 1),
                    ],
                    order="sequence asc",
                )
                if orders:
                    for index,sol in enumerate(orders,start=val["sequence"]+1):
                        sol.sequence = index
        return super().create(vals)
