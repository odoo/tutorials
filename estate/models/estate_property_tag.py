from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'The tag name already exists.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
