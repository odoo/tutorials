from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Name', required=True, translate=True)
    property_id = fields.One2many('estate.property', 'property_type_id', string='Property')

    _name_uniq = models.Constraint(
        'unique (name)',
        'There is already a Property Type with this name!.',
    )
