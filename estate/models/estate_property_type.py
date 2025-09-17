from odoo import fields, models 


class RealEstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _check_tag_name = models.Constraint(
    'UNIQUE(name)',
    'The type name must be unique.')
    