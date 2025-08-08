from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The type name must be unique.'),
    ]