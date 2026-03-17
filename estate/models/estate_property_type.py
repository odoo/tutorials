# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property Tag"

    name = fields.Char(required=True)
