from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _check_property_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property tag must be unique.'
    )
    