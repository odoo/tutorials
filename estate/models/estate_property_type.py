from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"


    name = fields.Char(required=True)

    _sql_constraints =[
        ('unique_property_type','unique(name)','The property type should be unique')
    ]
