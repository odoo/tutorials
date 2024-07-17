from odoo import fields, models

class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tags"

    name = fields.Char(required=True)

    _sql_constraints = [('check_name', 'UNIQUE(name)', 'The name must be unique.')]
