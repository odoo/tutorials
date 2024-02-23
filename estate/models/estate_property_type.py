from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type model"


    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'Type name should be unique')
    ]
