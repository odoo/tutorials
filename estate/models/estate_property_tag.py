from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(required=True)

    _unique_property_tag_name = models.Constraint(
        'UNIQUE(name)',
        'Tag name must be unique !'
    )
