from odoo import fields, models

class TypeModel(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"
    _order = "sequence, name"

    name = fields.Char('Property Types', required=True)

    property_ids = fields.One2many('estate_property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    

    _sql_constraints = [
        ('check_type_uniqueness', 'UNIQUE(name)',
         'The new property type should be unique')
    ]