from odoo import fields,models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(string="Title", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property type already exists.'),
    ]
