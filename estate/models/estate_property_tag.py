from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A property tag"
    _order = "name asc"

    name = fields.Char('Property tag', required=True)
    _unique_name = models.Constraint(
        'unique (name)',
        'A property tag name must be unique.'
    )
    color = fields.Integer('Color')
