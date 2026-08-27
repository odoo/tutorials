from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char("Property Tag Name", required=True)
    color = fields.Integer()

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property tag with the same name already exists.',
    )
