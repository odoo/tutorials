from odoo import  fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate is defined"

    name = fields.Char(required = True)
    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)', 'The Property type should be unique')
    ]