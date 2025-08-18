# Odoo Imports
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tags'
    _order = 'name'

    # -----------------------------
    # Fields
    # -----------------------------
    name = fields.Char(string='Property Tag', required=True, help='Name of the tag used to categorize or label properties.')
    color = fields.Integer(string='Color', help='Color code used to visually distinguish this tag.')

    # -----------------------------
    # SQL Constraints
    # -----------------------------
    _sql_constraints = [
        ('uniq_tag_name', 'unique(name)', 'Tag name must be unique.'),
    ]
