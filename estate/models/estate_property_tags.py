from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate/Property/Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=1)

    _sql_constraints = [
        ("property_tag_unique", "unique (name)", "The tag name must be unique")
    ]
