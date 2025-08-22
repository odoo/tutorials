from odoo import fields, models


class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_property_tag_name", "UNIQUE(name)", "Property Tag Name must be unique")
    ]
