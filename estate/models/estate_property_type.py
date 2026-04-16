from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="name", required=True)

    _name_check = models.UniqueIndex(
        ('name'),
        'Please provide unique type as it is already taken'
    )
