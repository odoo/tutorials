from odoo import fields, models

class RealEstateCategory(models.Model):
    _name = "real.estate.property.category"
    _description = "Table for Categories of properties"

    name = fields.Char(string = 'Category', required = True)

    #Adding Sql constraints to tag name for unique tag name
    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]
    