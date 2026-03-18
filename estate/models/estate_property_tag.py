from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = "A property tag"
    _order = 'name'

    name = fields.Char(string='Tag Name', required=True)
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique.'
    )
    color = fields.Integer()
