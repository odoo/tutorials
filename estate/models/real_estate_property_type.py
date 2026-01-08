from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = "sequence, name"

    name = fields.Char(string="Name")
    property_ids = fields.One2many("real_estate", "property_type_id", required=True)
    sequence = fields.Integer("Sequence")

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )
