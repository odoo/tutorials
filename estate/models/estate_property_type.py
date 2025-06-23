from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    # misc
    name = fields.Char(string='Type', required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique.')
    ]