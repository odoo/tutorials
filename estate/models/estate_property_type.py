from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties Types"

    name = fields.Char('Name', required=True, translate=True)
    properties_ids = fields.One2many("estate.property", "property_type_id", "Properties")

    _types_uniq = models.Constraint(
        'unique(name)',
        "The type name already exists",
    )
