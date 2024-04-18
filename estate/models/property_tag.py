from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag of a property"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', 'A property tag name must be unique')]

    name = fields.Char(required=True)
    color = fields.Integer()
