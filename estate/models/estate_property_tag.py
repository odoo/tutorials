from odoo import _, fields, models


class EsatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char()
    color = fields.Integer()

    _sql_constraints = [
        ('tag_unique','UNIQUE(name)','The name must be unique'),
    ]
