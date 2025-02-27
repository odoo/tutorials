# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ModularTypesWizard(models.TransientModel):
    _name = "modular.type.wizard"
    _description = "Wizard to Set Modular Types"

    modular_type_ids = fields.One2many(
        'modular.type.line', 'modular_type_id', string="Modular Types")

    def apply_changes(self):
        for wizard in self:
            for record in wizard.modular_type_ids:
                self.env["modular.types"].search([("id", "=", record.type_id)]).write(
                    {"quantity_multiplier": record.type_value}
                )
        return {"type": "ir.actions.act_window_close"}
