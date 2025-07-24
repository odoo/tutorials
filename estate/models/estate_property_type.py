from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    name = fields.Char(required = True)
    property_ids = fields.One2many(comodel_name="estate_property", inverse_name = "property_type_id")

    _sql_constraints = [
        ('is_property_type_unique', 'UNIQUE(name)', 'Property type name must be unique!')
    ]