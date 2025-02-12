from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char("Property Type", required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The Type name should be unique')
    ]
