from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Stores types of Property"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('check_property_type_name', 'UNIQUE(name)', 'Property Type name must be unique')
    ]
