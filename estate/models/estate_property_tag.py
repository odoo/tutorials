from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _sql_constraints = [
        (
            "check_unique_estate_property_tag",
            "unique(name)",
            "This Property Tag is already exists",
        )
    ]
    # --------------------------------------- Fields Declaration ----------------------------------
    # Basic Fields
    name = fields.Char("Tag", required=True)
    color = fields.Integer("Color index")
