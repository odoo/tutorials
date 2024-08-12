from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', name='Property Type Id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")


    _sql_constraints = [
        ('name_uniq', 'unique(name)',
        'A type with the same name already exists')
    ]
