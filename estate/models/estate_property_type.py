from odoo import fields, models

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    # Add the One2many field to store the related properties
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    #constraint
    _sql_constraints = [
        ("unique_property_type_name", "UNIQUE(name)", "The property type name must be unique."),
    ]