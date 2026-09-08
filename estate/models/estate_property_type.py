from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Estate Property Types"

    name = fields.Char("Property Type", required=True)
    property_id = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(string="Sequence", default=1)
    _order = "name asc"

    _check_type_name = models.Constraint(
        'UNIQUE(name)',
        'The type name should be unique.',
    )
