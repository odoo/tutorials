from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'unique(name)',
         'This type already exists.') 
    ]
