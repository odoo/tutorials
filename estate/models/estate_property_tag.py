from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _property_tag_unique_constraint = models.Constraint("UNIQUE(name)", "Property tag should have an unique name!")
