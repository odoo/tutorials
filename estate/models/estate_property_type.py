from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    _order = "sequence, name"

    name = fields.Char(required=True)

    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type must be unique!'),
    ]