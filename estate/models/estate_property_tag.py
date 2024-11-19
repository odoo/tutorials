from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_unique_name', 'unique(name)',
         'Tag name must be unique.'),
    ]
