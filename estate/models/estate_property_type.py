from odoo import fields,models # type: ignore

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type names must be unique.'),
    ]
