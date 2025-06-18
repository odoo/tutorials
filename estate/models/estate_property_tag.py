from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real estate property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "The tag already exists."),
    ]
