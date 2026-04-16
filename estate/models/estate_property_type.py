from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "A model where property types are defined"

    name = fields.Char(required=True, string="Property Type")
    property_ids = fields.One2many(
        'estate.property', inverse_name='property_type_id', string="Properties")
