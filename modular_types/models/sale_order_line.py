from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_modular_types = fields.Boolean(compute="_compute_has_modular_types", store=True)

    @api.depends("product_id.modular_type_ids")
    def _compute_has_modular_types(self):
        for line in self:
            line.has_modular_types = bool(line.product_id.modular_type_ids)

    def action_open_modular_values_wizard(self):
        self.ensure_one()
        return {
            "name": "set modular type values",
            "type": "ir.actions.act_window",
            "res_model": "set.modular.values.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_line_id": self.id,
                "default_line_ids": [
                    (
                        0,
                        0,
                        {"modular_type_id": m_type.id, "value": 1.0},
                    )
                    for m_type in self.product_id.modular_type_ids
                ],
            },
        }
