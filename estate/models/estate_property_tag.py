from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    # misc
    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]