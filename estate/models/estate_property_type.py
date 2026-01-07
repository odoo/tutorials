from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"

    name = fields.Char("Property Type", required=True)

    # SQL CONSTRAINT
    _property_type_uniq = models.Constraint(
        'UNIQUE(name)', "Property Type already exist in database"
    )
