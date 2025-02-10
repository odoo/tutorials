from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("estate_property_tag_check_name", "UNIQUE(name)", "The property tag name already exists!"),
    ]
