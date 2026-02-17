from odoo import fields, models


class SetModularValuesLineWizard(models.TransientModel):
    _name = "set.modular.values.line.wizard"
    _description = "Set Modular Type Value Line"

    wizard_id = fields.Many2one("set.modular.values.wizard", string="Wizard")
    modular_type_id = fields.Many2one("modular.type", string="Modular Type")
    value = fields.Float(string="Value", default=1.0)
