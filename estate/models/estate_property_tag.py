from odoo import fields, models  # pylint: disable=import-error


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(required=True)
    _unique_price = models.Constraint(
        'UNIQUE(name)',
        'Property tag must be unique'
    )

