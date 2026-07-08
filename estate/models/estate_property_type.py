from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "model for estate property types"
    name = fields.Char(required=True)
    _name_uniq = models.Constraint(
        'unique(name)',
        'A type with the same name already exists in property type.',
    )
