from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag an estate property'
    _sql_constraints = [('name_unique', 'UNIQUE(name)', "A property tag name must be unique")]

    name = fields.Char(required=True)
    