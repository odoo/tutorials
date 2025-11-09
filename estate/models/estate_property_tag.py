from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char("Estate Tag", required=True)
    color = fields.Integer('Color')
    _order = 'name desc'

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name of the tag should be unique.')
    ]
