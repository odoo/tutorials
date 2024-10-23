from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Model representing the different types of properties'

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', "This property type already exists."),
    ]
