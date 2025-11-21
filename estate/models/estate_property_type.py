from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties Types"
    _order = "name"
    name = fields.Char('Name', required=True, translate=True)
    properties_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    _types_uniq = models.Constraint(
        'unique(name)',
        "The type name already exists",
    )
