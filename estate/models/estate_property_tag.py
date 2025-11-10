from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _check_tag_name_unique = models.Constraint(
    'UNIQUE(name)', 
    'The name of the property tag must be unique.'
    )
