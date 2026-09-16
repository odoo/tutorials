# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags for the estate"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'The nae must be unique.',
    )
