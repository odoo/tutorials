from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _check_unique_type_name = models.Constraint('unique(name)',
                                                "You cannot enter a new Property Type with a duplicate name")

    property_ids = fields.One2many('estate.property', 'property_type_id')
