from odoo import fields, models

class TagModel(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer("Color", default=0)

    _sql_constraints = [
        ('check_tag_uniqueness', 'UNIQUE(name)',
         'The new tag should be unique')
    ]
