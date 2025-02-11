from odoo import fields, models


class PropertyTags(models.Model):
    _name = "property.tags"
    _description = "Property Tags"

    name = fields.Char(required=True)

    # sql constraints for unique tag name
    _sql_constraints = [
        ("unique_tag_name", "unique (name)", "Tag already exists!"),
    ]
