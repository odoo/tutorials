from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type object"

    name = fields.Char(required=True)

    _unique_name = models.UniqueIndex(
        '(name)',
        'name type must be unique',
    )
