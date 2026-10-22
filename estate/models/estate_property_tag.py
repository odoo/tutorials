from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _property_tag_name_uniq = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique'
    )
