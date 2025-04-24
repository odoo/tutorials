from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate type model"

    name = fields.Char(required=True)

    # One2Many relationships
    property_ids = fields.One2many('estate.property', 'property_type_id')
