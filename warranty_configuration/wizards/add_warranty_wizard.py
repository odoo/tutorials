from odoo import models, fields, api


class AddWarrantyWizard(models.TransientModel):
    _name = "add.warranty.wizard"
    _description = "Wizard to Add Warranty"

    order_id = fields.Many2one("sale.order", string="Sale Order")

    warranty_lines_ids = fields.One2many(
        comodel_name="add.warranty.line.wizard",
        inverse_name="warranty_id",
        string="Warranty Lines",
    )

    @api.model
    def default_get(self, fields):
        res = super(AddWarrantyWizard, self).default_get(fields)
        order_id = self.env.context.get("active_id")

        sale_order = self.env["sale.order"].browse(order_id)

        res["warranty_lines_ids"] = [
            [
                0,
                0,
                {
                    "sale_order_line_id": line.id,
                },
            ]
            for line in sale_order.order_line.filtered(
                lambda x: x.product_template_id.warranty
            )
        ]
        res["order_id"] = order_id

        return res

    def action_add_warranty(self):
        new_order_line_list = [
            {
                "order_id": line.sale_order_line_id.order_id.id,
                "name": str(line.warranty_config_id.name) + "/" + str(line.end_date),
                "price_unit": line.sale_order_line_id.price_subtotal
                * (line.warranty_config_id.percentage / 100),
                "product_id": line.warranty_config_id.product_id.id,
                "parent_sale_order_line_id": line.sale_order_line_id.id,
                "sequence": line.sale_order_line_id.sequence,
            }
            for line in self.warranty_lines_ids.filtered(
                lambda x: x.warranty_config_id.name
            )
        ]
        self.env["sale.order.line"].create(new_order_line_list)
