from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ('check_name', 'unique(name)',
         'This type already exists.') 
    ]

class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Estate property type line"

    property_id = fields.Many2one("estate.property")
    name = fields.Char()
    expected_price = fields.Float()
    state = fields.Char()
