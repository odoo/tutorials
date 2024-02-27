from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"
    _sql_constraints = [
        ('tag_name_unique', 'UNIQUE (name)', 'The name must be unique.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
