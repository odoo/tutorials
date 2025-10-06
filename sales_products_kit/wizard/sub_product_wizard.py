from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class SubProductWizard(models.TransientModel):
    _name = "sub.product.wizard"
    _description = "A wizard the display sub-product included in the kit."

    sale_order_line_id = fields.Many2one(
        "sale.order.line", required=True, ondelete="cascade"
    )
    line_ids = fields.One2many(
        comodel_name="sub.product.line",
        inverse_name="sub_product_wizard_id",
        string="Sub Products",
        required=True,
    )

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        sale_order_line_id = self.env.context.get("default_sale_order_line_id")
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
        product_template = sale_order_line.product_template_id
        existing_wizard = self.env["sub.product.wizard"].search(
            [("sale_order_line_id", "=", sale_order_line_id)]
        )

        if existing_wizard:
            defaults.update(
                {
                    "sale_order_line_id": sale_order_line_id,
                    "line_ids": existing_wizard.line_ids,
                }
            )
        else:
            line_data = []
            for sub_product in product_template.sub_product_ids:
                line_data.append(
                    Command.create(
                        {
                            "product_id": sub_product.id,
                            "quantity": 1,
                            "price_unit": sub_product.lst_price,
                        }
                    )
                )

            defaults.update(
                {
                    "sale_order_line_id": sale_order_line_id,
                    "line_ids": line_data,
                }
            )
        return defaults

    def action_confirm(self):
        if sum(self.line_ids.mapped("quantity")) == 0:
            raise UserError(
                "You must select atleast 1 sub-product to purchase the kit product."
            )

        lines_to_create = []
        total_price = 0

        for line in self.line_ids:
            if line.quantity > 0:
                existing_line = self.env["sale.order.line"].search(
                    [
                        ("order_id", "=", self.sale_order_line_id.order_id.id),
                        ("product_id", "=", line.product_id.id),
                        ("parent_line_id", "=", self.sale_order_line_id.id),
                    ],
                    limit=1,
                )

                if existing_line:
                    existing_line.product_uom_qty = line.quantity
                    existing_line.price_unit = 0.0
                else:
                    lines_to_create.append(
                        {
                            "order_id": self.sale_order_line_id.order_id.id,
                            "product_id": line.product_id.id,
                            "product_uom_qty": line.quantity,
                            "price_unit": 0.0,
                            "parent_line_id": self.sale_order_line_id.id,
                        }
                    )
                total_price += line.quantity * line.price_unit

        if lines_to_create:
            self.env["sale.order.line"].create(lines_to_create)

        self.sale_order_line_id.price_unit = total_price
        return True
