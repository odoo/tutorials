from odoo import fields, models

class EstatePropertyType(models.Model):
    # model definition
    _name = "estate.property.type"
    _description = "property type model"

    # normal fields
    name = fields.Char(required=True)
