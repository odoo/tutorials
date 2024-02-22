from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=2)

    _sql_constraints = [
        ('check_property_tag_name', 'UNIQUE (name)', 'Property tag already exists.')
    ]
    