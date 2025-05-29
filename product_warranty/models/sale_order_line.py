from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty = fields.Boolean(default=False)
    warranty_product_id = fields.Many2one("product.warranty")
    warranty_orderline = fields.Many2one("sale.order.line", ondelete="cascade")
    products = fields.Many2one("sale.order.line")
    is_warranty = fields.Boolean(default=False)

    @api.ondelete(at_uninstall=False)
    def _unlink_warranty(self):
        for record in self:
            if record.warranty and record.warranty_orderline:
                record.warranty_orderline.unlink()

    @api.ondelete(at_uninstall=False)
    def _unlink_warranty_from_product(self):
        for record in self:
            if record.is_warranty and record.products:
                record.products.write(
                    {
                        "warranty": False,
                        "warranty_product_id": None,
                        "warranty_orderline": None,
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("is_warranty", False):
                orders = self.env["sale.order.line"].search(
                    [
                        ("order_id", "=", val["order_id"]),
                        ("sequence", ">=", val["sequence"]),
                    ],
                    order="sequence asc",
                )
                for index, sol in enumerate(orders, start=val["sequence"] + 1):
                    sol.sequence = index
        return super().create(vals_list)
