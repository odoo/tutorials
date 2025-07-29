#!/usr/bin/env python3

from odoo import models, fields
from typing import final


@final
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for a property"
    _order = "name asc"

    name = fields.Char(required=True)

    _sql_constraints: list[tuple[str, str, str]] = [
        (
			"unique_name",
			"UNIQUE (name)",
			"Tag name should be unique",
		),
    ]
