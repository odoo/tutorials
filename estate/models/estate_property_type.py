from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties Types"

    name = fields.Char('Name', required=True, translate=True)

    _types_uniq = models.Constraint(
        'unique(name)',
        f"The type name already exists",
    )