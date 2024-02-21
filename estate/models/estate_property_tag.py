from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Tag name must be unique.')
    ]
