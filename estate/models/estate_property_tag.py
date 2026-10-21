from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag object"

    name = fields.Char(required=True)

    _unique_name = models.UniqueIndex(
        '(name)',
        'name tag must be unique',
    )
