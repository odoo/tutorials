from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag of a property"

    name = fields.Char(required=True)
    _sql_constraints = [('name_unique', 'unique(name)', 'A property tag name must be unique')]

    