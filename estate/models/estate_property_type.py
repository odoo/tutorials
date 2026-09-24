from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property.type"
    _description = "Types of Estate Property"
    _order = "name"

    name = fields.Char('Nom', required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id', "Property")
    sequence = fields.Integer(string="Sequence", default=1)
    _check_unique_name = models.Constraint(
        "UNIQUE (name)",
        "The name must be unique",
    )
