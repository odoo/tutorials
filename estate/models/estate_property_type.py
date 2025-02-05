from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This has all the property types"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ("uniq_type", "unique(name)", "Types should have a unique name.")
    ]
