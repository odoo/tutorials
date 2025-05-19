from odoo import api, fields, models


class addWarrantyWizard(models.TransientModel):
    _name = "warranty.wizard"
    _description = "Wizard to add Warranty for product"

    sale_order_id = fields.Many2one("sale.order", string="Quotation", required=True)
    line_ids = fields.One2many("warranty.wizard.line", "wizard_id", string=" ")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))
        lines = []

        for line in sale_order.order_line:
            if line.product_id.is_warranty_available:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                            "sale_order_line_id": line.id,
                        },
                    )
                )
        res["sale_order_id"] = sale_order.id
        res["line_ids"] = lines
        return res

    def action_add_warranty_product(self):
        total_price = 0
        description_lines = []
        linked_lines = None
        warranty_product = None

        for line in self.line_ids:
            if line.warranty_id:
                base_price = line.sale_order_line_id.price_unit
                percentage = line.warranty_id.percentage
                extended_price = (base_price * percentage) / 100
                total_price += extended_price

                description_lines.append(
                    f"{line.product_id.name} - Valid till {line.warranty_end_date}"
                )

                if not warranty_product:
                    warranty_product = line.product_id

                linked_lines = line.sale_order_line_id.id

        if total_price > 0:
            self.env["sale.order.line"].create(
                {
                    "order_id": self.sale_order_id.id,
                    "product_id": warranty_product.id,
                    "name": "Extended Warranty:\n" + "\n".join(description_lines),
                    "price_unit": total_price,
                    "product_uom_qty": 1,
                    "product_uom": warranty_product.uom_id.id,
                    "linked_sale_order_line_id": linked_lines,
                }
            )
