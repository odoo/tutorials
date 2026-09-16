# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types of the estate"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'The nae must be unique.',
    )
