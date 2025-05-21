from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"

    name = fields.Char(required=True)

    _sql_constraints = [('check_estate_property_tag_unique', 'UNIQUE (name)', 'The name must be unique.')]
