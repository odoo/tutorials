from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)

    _name_uniq = models.Constraint(
        'unique (name)',
        'There is already a Property Tag with this name!.',
    )
