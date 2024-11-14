from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_name', 'unique(name)',
         'Tag name must be unique.'),
    ]