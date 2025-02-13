from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=1)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Tag name must be unique')
    ]
