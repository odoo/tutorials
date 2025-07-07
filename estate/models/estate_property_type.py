from odoo import fields,models

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Types of Real Estate Properties"

    name = fields.Char(required=True, string="Property Type")