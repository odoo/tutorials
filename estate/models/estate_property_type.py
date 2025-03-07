from odoo import fields, models

class estate_Property_Type(models.Model):
    _name = "estate.property.type"
    _description = "relevent type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)','The name must be unique.')
    ]
