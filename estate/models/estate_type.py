from odoo import fields, models

class EstateTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property types"
    _sql_constraints = [('check_name', 'UNIQUE(name)', "The name must be unique.")]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type', required=True)
