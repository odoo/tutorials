from odoo import api, fields, models


class saleOrderLineWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    _description = "Set Modular Type Values Wizard"

    order_line_id = fields.Many2one(
        "sale.order.line", string="Order Line", required=True
    )
    modular_type_value_ids = fields.One2many(
        "modular.type.value.wizard", "wizard_id", string=" ", required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        order_line = self.env["sale.order.line"].browse(
            self.env.context.get("active_id")
        )
        values = []

        for modular_val in order_line.product_template_id.modular_type_ids:
            values.append((0, 0, {"modular_type_id": modular_val.id, "value": 0}))

        res.update({"order_line_id": order_line.id, "modular_type_value_ids": values})

        return res

    def apply_values(self):
        self.order_line_id.modular_type_value_ids.unlink()

        for line in self.modular_type_value_ids:
            self.env["sale.order.line.modular.type"].create(
                {
                    "order_line_id": self.order_line_id.id,
                    "modular_type_id": line.modular_type_id.id,
                    "value": line.value,
                }
            )

        return {"type": "ir.actions.act_window_close"}
