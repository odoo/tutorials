from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property tag should be unique.',
    )
