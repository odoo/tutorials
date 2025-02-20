from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'the tag of the property being sold'

    name = fields.Char(required = True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tag name must be unique!')
    ]
