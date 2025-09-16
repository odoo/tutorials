from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)

    _name_unique = models.Constraint('UNIQUE(name)', 'The tag name must be unique.')
