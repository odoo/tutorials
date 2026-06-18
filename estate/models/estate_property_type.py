from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
    )
    _unique_name = models.Constraint(
        "UNIQUE(name)", "Property type name must be unique."
    )
