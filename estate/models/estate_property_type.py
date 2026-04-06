from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "sequence, name"
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique',
    )

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)

    property_ids = fields.One2many("estate.property", "property_type_id", string="property type")
