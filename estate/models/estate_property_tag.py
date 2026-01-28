from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Information'
    _order = 'name asc'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string="Color")

    _check_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.'
    )
