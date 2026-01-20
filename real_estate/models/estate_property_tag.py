from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property tag name must be unique')
    ]