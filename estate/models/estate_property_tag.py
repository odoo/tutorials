from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    
    name = fields.Char(required=True)
    
    # SQL Constraints
    
    sql_constraints = [
        (
            "unique_property_tag_name",
            "UNIQUE(name)",
            "The name of the tag must be unique.",
        ),
    ]