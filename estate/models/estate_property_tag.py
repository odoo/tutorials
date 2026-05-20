from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    # SQL constraints
    _unique_tag_name = models.Constraint(
        'UNIQUE(name)', 
        "A property tag name must be unique."
    )
    