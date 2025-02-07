from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate properties type"
    _order = "sequence, name"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type', readonly=True)
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('type_name_unique', 'unique(name)',
         'The type name must be unique.'),
    ]
