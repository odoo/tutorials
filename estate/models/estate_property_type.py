from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    _name_unique = models.Constraint(
        'unique(name)',
        '2 property type names cannot be same '
    )
    property_id = fields.One2many("estate.property", "property_type_id", string="properties")
    sequence = fields.Integer(string="Sequence")
    color = fields.Integer()
