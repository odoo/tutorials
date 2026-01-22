from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Name', required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type names should be unique'
    )

class EstatePropertyTypeLine(models.Model):
    _name = 'estate_property_type_line'
    _description =  'Estate Property Type Line'

    property_type_id = fields.Many2one('estate.property.type')
