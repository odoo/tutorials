from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Phis model provides tags for estate property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint(
        'unique(name)',
        "A property tag name must be unique.",
    )
