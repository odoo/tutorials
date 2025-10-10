
from odoo import fields, models


# estate.property.tag model
class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag database table"
    _order = "name"

    name = fields.Char(string="Tag name", required=True)
    color = fields.Integer()
    _sql_constraints = [
        (
            "unique_property_tag",
            "unique(name)",
            "Property tag should be unique",
        ),
    ]
