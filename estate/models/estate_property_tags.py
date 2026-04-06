from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tags"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag with this name already exists.',
    )
