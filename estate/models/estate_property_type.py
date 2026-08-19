from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence"

    name = fields.Char('Type Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many("estate.property", "type_id")

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        'The type name must be unique'
    )
