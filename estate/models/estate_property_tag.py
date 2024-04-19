from odoo import fields, models

class PropertyTag(models.Model):

    _name = "estate_property_tag"
    _description = "The tags that can be assigned to the property i.e. cozy, renovated, etc"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The tag name must be unique'),
    ]
    name = fields.Char(required=True)
