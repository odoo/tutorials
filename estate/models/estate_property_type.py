from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties"
    _check_type_name = models.Constraint("UNIQUE(name)", "Type names must be unique.")
    _order = 'sequence, name asc'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types")

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
