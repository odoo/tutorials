from odoo import models, fields


class PropertyTags(models.Model):

    _name = "estate.property.tag"
    _description = "Tags for properties in the Estate app"

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'The Tag\'s names should be unique')]
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
