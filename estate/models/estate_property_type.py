from odoo import fields, models  # pylint: disable=import-error


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
    )
    _unique_name = models.Constraint(
        "UNIQUE(name)", "Property type name must be unique."
    )

