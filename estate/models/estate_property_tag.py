from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this model provides tags for estate property"
    name = fields.Char(required=True)
    _name_uniq = models.Constraint(
        'unique(name)',
        'A tag with the same name already exists in property tag.',
    )
