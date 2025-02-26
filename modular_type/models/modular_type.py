# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ModularType(models.Model):
    _name = "modular.types"
    _description = "Modular Types"

    name = fields.Char("Modular Type")
    quantity_multiplier = fields.Integer("Multiplier", default=0)
    color = fields.Integer("color", default=0)
