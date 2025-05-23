from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(default=1, help="Used to order types. Lower is better.")

    # Foreign keys
    property_ids = fields.One2many("estate.property", "property_type_id")
