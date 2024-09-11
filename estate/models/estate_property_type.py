from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = 'sequence ASC, name ASC'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types")    
    property_ids  = fields.One2many("estate.property", "property_type")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]
