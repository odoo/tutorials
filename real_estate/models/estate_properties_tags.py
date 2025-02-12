from odoo import fields, models


class EstatePropertiesTags(models.Model):
    _name = 'estate.properties.tags'
    _description = 'Estate Properties Tags'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'Tag Name should be unique')
    ]
