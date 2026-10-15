from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type should be unique.',
    )
