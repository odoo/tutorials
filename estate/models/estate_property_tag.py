from odoo import _, fields, models


class EsatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char()

    _sql_constraints = [
        ('tag_unique','UNIQUE(name)','The name must be unique'),
    ]
