from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence,name"

    name = fields.Char()
    sequence = fields.Integer(
        string="Sequence",
        default=1,
        help="Used to order property types manually."
    )

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique!',
    )
