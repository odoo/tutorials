from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Tags for properties"
    _order = "name "
    name = fields.Char(string="Tags")
    color = fields.Integer(string="Color")

    _unique_property_tag = models.Constraint(
        'UNIQUE(name)',
        'Property Tag must be unique'
    )
