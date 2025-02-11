from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(
        string="Color Id", default=1, help="It will use to define colors automatically"
    )
    _sql_constraints = [
        (
            "unique_property_tag_name",
            "UNIQUE(name)",
            "Property tag name must be unique!",
        )
    ]


