from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define type of properties'
    _sql_constraints = [('name_unique', 'UNIQUE(name)', "A property type name must be unique")]

    name = fields.Char(required=True)
    