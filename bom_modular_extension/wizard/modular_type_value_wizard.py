from odoo import fields, models


class modularTypeValueWizard(models.TransientModel):
    _name = "modular.type.value.wizard"
    _description = "Set Modular Type Value Wizard"

    wizard_id = fields.Many2one("sale.order.line.wizard", string="Wizard")
    modular_type_id = fields.Many2one(
        "modular.type", string="Modular Type", required=True
    )
    value = fields.Float(string="Value", required=True)
