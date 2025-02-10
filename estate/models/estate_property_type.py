from odoo import fields, models

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="estate property type table"
    # _order="name asc"

    name= fields.Char("Property Type", required=True) 

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]

    property_ids = fields.One2many("estate.property", "property_type_id", readonly=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")