from odoo import models, fields


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence,name"

    name = fields.Char("Property Type Name", required=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is ranked higher.")

    properties = fields.One2many(comodel_name="estate.property", inverse_name="type")

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property type with the same name already exists.',
    )
