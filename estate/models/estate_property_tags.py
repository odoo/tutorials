from odoo import fields, models


class PropertyTags(models.Model):
    _name = "property.tags"
    _description = "Property Tags"
    _order = "name"

    # sql constraints for unique tag name
    _sql_constraints = [
        ("unique_tag_name", "unique (name)", "Tag already exists!"),
    ]

    # Fields
    name = fields.Char(required=True)
    color = fields.Integer(string="Color", help="Color code for the tag", default=8)
