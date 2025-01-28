from odoo import fields, models

class house_type(models.Model):
    _name = 'estate.house_type'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE name', 'type name value is already exisiting')
    ]

    name = fields.Char(required=True)
