from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate_property_type'
    _unique_type = models.UniqueIndex("(name)",'property type should be unique')

    name = fields.Char(required=True)
