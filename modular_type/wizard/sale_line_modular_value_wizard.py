from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleLineModularValueWizard(models.TransientModel):
    _name = "sale.line.modular.value.wizard"
    _description = "Sale Line Modular Value Wizard"

    sale_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        required=True,
    )

    line_ids = fields.One2many(
        "sale.line.modular.value.wizard.line",
        "wizard_id",
        string="Modular Values",
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        sale_line_id = self.env.context.get("default_sale_line_id")
        if not sale_line_id:
            return res

        sale_line = self.env["sale.order.line"].browse(sale_line_id)

        modular_types = sale_line.product_id.product_tmpl_id.modular_type_ids
        if not modular_types:
            raise UserError("Please configure Modular Types on the selected product first.")

        existing_values = {}
        for v in sale_line.modular_value_ids:
            existing_values[v.modular_type_id.id] = v.value

        lines = []
        for modular_type in modular_types:
            value = existing_values.get(modular_type.id, 1.0)
            lines.append((0, 0, {
                "modular_type_id": modular_type.id,
                "value": value,
            }))

        res["line_ids"] = lines
        return res

    def action_save(self):
        self.ensure_one()

        valid_lines = self.line_ids.filtered(lambda line: line.modular_type_id)

        if not valid_lines:
            raise UserError(
                "No modular types found. Please configure Modular Types on the product first."
            )

        self.sale_line_id.modular_value_ids.unlink()

        for line in valid_lines:
            self.env["sale.order.line.modular.value"].create({
                "sale_line_id": self.sale_line_id.id,
                "modular_type_id": line.modular_type_id.id,
                "value": line.value,
            })

        return {"type": "ir.actions.act_window_close"}


class SaleLineModularValueWizardLine(models.TransientModel):
    _name = "sale.line.modular.value.wizard.line"
    _description = "Sale Line Modular Value Wizard Line"

    wizard_id = fields.Many2one(
        "sale.line.modular.value.wizard",
        required=True,
        ondelete="cascade",
    )

    modular_type_id = fields.Many2one(
        "modular.type",
        string="Modular Type",
        required=True,
        readonly=True,
    )

    value = fields.Float(
        string="Value",
        default=1.0,
        required=True,
    )
