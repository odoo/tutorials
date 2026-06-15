from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    _name_unique = models.Constraint(
        "UNIQUE(name)", "Property Type name must be unique."
    )
