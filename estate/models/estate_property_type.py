from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'the type name must be unique')
    ]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
