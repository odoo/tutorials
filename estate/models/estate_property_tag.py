from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate properties tag"
    _order = "name"
    _sql_constraints = [
        ('tag_name_unique', 'unique(name)',
         'The tag name must be unique.'),
    ]

    name = fields.Char('Tag', required=True)
    color = fields.Integer('Color')
    rating = fields.Float('Ratings')
