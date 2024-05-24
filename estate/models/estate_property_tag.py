from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate property Tag"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_unique', 'UNIQUE(name)',
         'Value must be unique.')
    ]
