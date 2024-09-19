from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('property_tag_name_unique', 'UNIQUE(name)', 'Property tag name must be unique')
    ]
