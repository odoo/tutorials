from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate_property_tag description"
    _sql_constraints = [
        ('check_tag_name', 'unique(name)', 'A property tag name must be unique.')
    ]
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
