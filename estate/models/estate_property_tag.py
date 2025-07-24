from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_unique_tag_name', 'UNIQUE(name)',
         'The tag names need to be unique.'),
    ]
