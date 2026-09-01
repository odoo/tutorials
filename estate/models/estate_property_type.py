from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _name_uniq = models.Constraint(
        'unique(name)',
        'Property type name must be unique.',
    )
