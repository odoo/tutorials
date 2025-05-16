from odoo import models, fields


class EstatePropertyTag(models.Model):
    """Model representing tags for categorizing real estate properties.

    This model defines tags that can be associated with properties to describe
    characteristics or features.
    """

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name must be unique."),
    ]
