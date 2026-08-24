
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Model'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
    _check_name = models.Constraint('unique(name)', 'Name must be set')
