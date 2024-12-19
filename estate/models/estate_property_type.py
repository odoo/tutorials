from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types for real state properties'

    name = fields.Char(required=True)
