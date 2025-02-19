from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate"

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Name must be unique.'),
    ]

    _order = "sequence,name"
