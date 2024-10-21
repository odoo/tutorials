from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char("Tag", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        (
            'Unique_property_tag_name',
            'UNIQUE(name)',
            'A property tag name must be unique'
        )
    ]
