from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name'

    _unique_name = models.Constraint(
        'unique(name)',
        "Property tag name must be unique.",
    )

    name = fields.Char("Property Tag", required=True)
    color =fields.Integer("Color")
