from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Property Type", required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'Types should have unique names.'),
    ]
