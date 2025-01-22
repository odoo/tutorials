from odoo import fields, models

class TagModel(models.Model):
    _name = "estate_property_tag"
    _description = "estate property tag"

    name = fields.Char('Property Tags', required=True)

    _sql_constraints = [
        ('check_tag_uniqueness', 'UNIQUE(name)',
         'The new tag should be unique')
    ]
    