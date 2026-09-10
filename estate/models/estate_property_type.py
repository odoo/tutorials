from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _rec_name = 'property_name'

    property_name = fields.Char(required=True)
