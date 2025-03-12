from odoo import api, fields, models


class ModularTypeWizard(models.TransientModel):
    _name = "modular.type.wizard"
    _description = "Set Modular Type Values"

    sale_order_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
    modular_types_line = fields.One2many(
        "modular.type.line.wizard", "wizard_id", string="Modular Types"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order_line_id = self.env.context.get("active_id")
        sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)

        if sale_order_line and sale_order_line.product_id:
            existing_modular_values = {
                val.modular_type_id.id: val.value
                for val in sale_order_line.modular_type_values
            }
            module_lines = []

            for modular_type in sale_order_line.product_id.product_tmpl_id.modular_types:
                module_lines.append(
                    (
                        0,
                        0,
                        {
                            "modular_type_id": modular_type.id,
                            "value": existing_modular_values.get(modular_type.id, 0),
                        },
                    )
                )

            res.update(
                {
                    "sale_order_line_id": sale_order_line_id,
                    "modular_types_line": module_lines,
                }
            )

        return res

    def apply_modular_values(self):
        self.ensure_one()

        if not self.sale_order_line_id:
            return
        existing_modular_values = {}  
        for val in self.sale_order_line_id.modular_type_values:  
            existing_modular_values[val.modular_type_id.id] = val  


        for line in self.modular_types_line:
            if line.modular_type_id.id in existing_modular_values:
                # Update the existing record
                existing_modular_values[line.modular_type_id.id].write(
                    {"value": line.value}
                )
            else:
                # Create a new modular value entry if not already present
                self.sale_order_line_id.write(
                    {
                        "modular_type_values": [
                            (
                                0,
                                0,
                                {
                                    "modular_type_id": line.modular_type_id.id,
                                    "value": line.value,
                                },
                            )
                        ]
                    }
                )


class ModularTypeLineWizard(models.TransientModel):
    _name = "modular.type.line.wizard"
    _description = "Modular Type Line Wizard"

    wizard_id = fields.Many2one(
        "modular.type.wizard", string="Wizard", required=True, ondelete="cascade"
    )
    modular_type_id = fields.Many2one(
        "module.types", string="Modular Type"
    )
    value = fields.Float(string="Value", default=1.0, required=True)
