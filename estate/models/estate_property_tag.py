from odoo import fields
from odoo import models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property tag"
    _order = "name asc"
    # Constraints
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The property type name must be unique'),
    ]

    name = fields.Char("Tag", required=True, translate=True)
    description = fields.Text("Tag description")
    color = fields.Integer()
