from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tags'
    _check_name = models.Constraint('UNIQUE(name)', 'Tag name must be unique')

    name = fields.Char('Name', required=True)
