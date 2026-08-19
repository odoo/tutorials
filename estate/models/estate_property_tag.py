
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Model'

    name = fields.Char(required=True)
    _check_name = models.Constraint('unique(name)', 'Name must be set')
