# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AnimalType(models.Model):
    _name = "shelter.animal_type"
    _description = "Type"

    name = fields.Char(required=True)
    pictogram = fields.Image("Pictogram")
