# -*- coding: utf-8 -*-

from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = 'estate_property_tags'
    _description = 'Real Estate Property Tags'

    name = fields.Char()

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE (name)', 'Tag name already exists!'),
    ]
