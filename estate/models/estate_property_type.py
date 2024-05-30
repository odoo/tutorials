# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    _sql_constraints = [(
        'check_unique_name',
        'UNIQUE(name)',
        'this name already exists!')
    ]

    property_ids = fields.One2many(
        'estate_property',
        'property_type_id',
        string='Properties'
    )
