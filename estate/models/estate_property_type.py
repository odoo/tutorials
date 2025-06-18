from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "This property type already exists."),
    ]
