from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         'The property tag name must be unique.'
         )
    ]

    # misc
    name = fields.Char(required=True)
    color = fields.Integer(string='Color')
