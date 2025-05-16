from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_info_line_ids = fields.One2many(
        "sale.order.global.info",
        "sale_order_id",
        string="Global Info Details",
        readonly=False,
    )

    def update_global_info(self):
        """Automatically update global info lines when order is created or modified"""
        for order in self:
            existing_info = {
                info.attribute_id.id for info in order.global_info_line_ids
            }
            category_data = []

            categories = self.env["product.category"].search(
                [("show_global_info", "=", True)]
            )

            for category in categories:
                for attribute in category.attribute_ids:
                    if attribute.id not in existing_info:
                        category_data.append(
                            (
                                0,
                                0,
                                {
                                    "sale_order_id": order.id,
                                    "category_name": category.name,
                                    "attribute_id": attribute.id,
                                },
                            )
                        )

            if category_data:
                order.global_info_line_ids = category_data

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure global info updates when creating a sale order"""
        orders = super().create(vals_list)
        orders.update_global_info()
        return orders

    def write(self, vals):
        """Ensure global info updates when modifying a sale order"""
        result = super().write(vals)
        if "order_line" in vals or "global_info_line_ids" in vals:
            self.update_global_info()
        return result


class SaleOrderGlobalInfo(models.Model):
    _name = "sale.order.global.info"
    _description = "Sale Order Global Info"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", ondelete="cascade"
    )
    category_name = fields.Char(string="Product Category", required=True)

    attribute_id = fields.Many2one(
        "product.attribute", string="Attribute", required=True
    )

    attribute_value_id = fields.Many2one(
        "product.attribute.value",
        string="Attribute Value",
        domain="[('attribute_id', '=', attribute_id)]",
    )
