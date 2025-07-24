#!/usr/bin/env python3

from odoo import models, fields
from typing import final


@final
class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for a property"
    name = fields.Char(required=True)
