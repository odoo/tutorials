from odoo import fields, models

class PropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'A property tag name must be unique.')
    ]