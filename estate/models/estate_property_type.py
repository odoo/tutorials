from odoo import fields, models


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_name', 'unique(name)',
         'Type name must be unique.'),
    ]