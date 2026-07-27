from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "A list of tags that categorize the properities"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property tag names must be unique!",
    )
