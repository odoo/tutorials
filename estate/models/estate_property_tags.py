from odoo import fields, models


class EstatePropertyTagsModel(models.Model):
    _name = "estate.property.tags"
    _description = "The estate property tags model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_property_tag", "UNIQUE(name)", "The property tag name must be unique")
    ]
