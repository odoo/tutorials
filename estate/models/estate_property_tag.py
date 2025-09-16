from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer('Color')

    _name_unique = models.Constraint('UNIQUE(name)', "The tag name must be unique.")
