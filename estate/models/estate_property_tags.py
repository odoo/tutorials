from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate/Property/Tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("property_tag_unique", "unique (name)", "The tag name must be unique")
    ]
