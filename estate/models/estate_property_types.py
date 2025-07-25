from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.types"
    _description = " Estate Property Types"
    _order = "name"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")

    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)',
         'The property type must be unique!!')
    ]
