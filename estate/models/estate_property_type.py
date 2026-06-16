from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Properties",
    )
    sequence = fields.Integer(
        "Sequence", default="1"
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)', "Property Type name must be unique."
    )
