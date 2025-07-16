from odoo import  fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property type is defined"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('property_type_unique','unique(name)','property type should be unique')
    ]