from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Information'

    name = fields.Char(string='Tag Name', required=True)

    _check_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.'
    )
