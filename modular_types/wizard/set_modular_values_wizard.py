from odoo import fields, models


class SetModularValuesWizard(models.TransientModel):
    _name = "set.modular.values.wizard"
    _description = "Set Modular Type Values"

    sale_line_id = fields.Many2one("sale.order.line", string="Sale Line")
    line_ids = fields.One2many(
        "set.modular.values.line.wizard", "wizard_id", string="Values"
    )

    def action_confirm(self):
        self.ensure_one()
        self.sale_line_id.modular_value_ids.unlink()
        vals = []
        for line in self.line_ids:
            vals.append(
                (
                    0,
                    0,
                    {"modular_type_id": line.modular_type_id.id, "value": line.value},
                )
            )
        self.sale_line_id.write({"modular_value_ids": vals})
        return {"type": "ir.actions.act_window_close"}
