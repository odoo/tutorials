from odoo import fields, models


class AwesomeEstatePropertyTag(models.Model):
    _name = 'awesome.estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.',
    )
