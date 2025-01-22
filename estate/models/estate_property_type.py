from odoo import fields, models

class TypeModel(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"

    name = fields.Char('Property Types', required=True)
    

    _sql_constraints = [
        ('check_type_uniqueness', 'UNIQUE(name)',
         'The new property type should be unique')
    ]