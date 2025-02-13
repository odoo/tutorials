from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name asc'

    name = fields.Char(
        string="Tag",
        required=True
    )
    color = fields.Integer(
        string="Color",
        default=5
    )

    # SQL CONSTRAINTS
    _sql_constraints = [
        (
            'unique_tag_name',
            'UNIQUE(name)',
            'Property Tag name must be Unique.'
        )
    ]
