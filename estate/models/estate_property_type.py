from odoo import fields, models


class EsatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('type_unique','UNIQUE(name)','The name must be unique'),
    ]
