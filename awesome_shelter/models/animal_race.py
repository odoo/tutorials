# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AnimalRace(models.Model):
    _name = "awesome_shelter.animal_race"
    _description = "Race"

    name = fields.Char(required=True)
