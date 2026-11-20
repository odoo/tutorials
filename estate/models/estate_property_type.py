from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ESTATE property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', "property_type", string="Properties")
    sequence = fields.Integer('Sequence', default=1)
