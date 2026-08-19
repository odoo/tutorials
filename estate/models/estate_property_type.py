from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Name', required=True, translate=True)

    _name_uniq = models.Constraint(
        'unique (name)',
        'There is already a Property Type with this name!.',
    )
