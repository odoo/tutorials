""" A module defining the tags that can be attached to a real estate property"""

from odoo import fields, models

class PropertyTag(models.Model):
    """
    Represents the tags of a real estate property such as
    cozy, renovated, etc.
    """
    _name = "estate_property_tag"
    _description = "The tags that can be assigned to the property i.e. cozy, renovated, etc"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The tag name must be unique'),
    ]
    _order = 'name'
    name = fields.Char(required=True)
    color = fields.Integer()
