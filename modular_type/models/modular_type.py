# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ModularType(models.Model):
    _name = "modular.types"
    _description = "Modular Types"

    name = fields.Char("Modular Type")
    quantity_multiplier = fields.Integer("Multiplier", default=0)
    color = fields.Integer("color", default=0)

    @api.constrains("quantity_multiplier")
    def _check_quantity_multiplier(self):
        for record in self:
            if record.quantity_multiplier < 0:
                raise ValidationError( _("Quantity multiplier must be greater than 0"))
