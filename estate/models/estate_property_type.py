#!/usr/bin/env python3
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _check_type_name = models.Constraint(
        "UNIQUE(name)", "A property type name should be unique."
    )

    name = fields.Char(required=True)
