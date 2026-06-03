from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    modular_value_ids = fields.One2many(
        "sale.order.line.modular.value",
        "sale_line_id",
        string="Modular Values",
    )

    def action_open_modular_value_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Set Modular Values",
            "res_model": "sale.line.modular.value.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_line_id": self.id,
            },
        }

    def _apply_modular_values_to_productions(self):
        for line in self:
            productions = self.env["mrp.production"].search([
                ("origin", "=", line.order_id.name),
                ("product_id", "=", line.product_id.id),
            ])

            modular_values = {
                v.modular_type_id.id: v.value
                for v in line.modular_value_ids
            }

            for move in productions.move_raw_ids.filtered(
                lambda m: m.bom_line_id.modular_type_id
            ):
                multiplier = modular_values.get(
                    move.bom_line_id.modular_type_id.id
                )

                if multiplier is not None:
                    move.product_uom_qty = move.bom_line_id.product_qty * multiplier
                else:
                    move.product_uom_qty = 0.0
