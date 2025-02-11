from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type'
    _order = 'sequence, name'

    _sql_constraints =[
        ('_unique_name','UNIQUE(name)','Property type must be unique'),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer(default=1, help='helps in ordering of views in ui')
