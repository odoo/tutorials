# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ModularTypeWizardLine(models.TransientModel):
    _name = "modular.type.line"
    _description = "Modular Type Wizard Line"

    modular_type_id = fields.Many2one(
        "modular.type.wizard", string="Modular Types"
    )
    type_id = fields.Integer(string="Type ID")
    type_name = fields.Char(string="Type Name")
    type_value = fields.Integer(string="Value")

    @api.constrains("type_value")
    def _check_type_value(self):
        for record in self:
            if record.type_value < 0:
                raise ValidationError(_("Value must be greater than 0"))
