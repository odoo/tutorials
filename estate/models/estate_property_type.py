from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property test model'
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id")
    sequence = fields.Integer()
